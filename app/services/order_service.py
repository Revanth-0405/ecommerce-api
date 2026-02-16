import json
import uuid
import os
from datetime import datetime
from threading import Lock

from app.models.product_model import Product
from app.db import db
from app.utils.error_handler import error_response


# Environment safe orders file
ORDERS_FILE = os.getenv("ORDERS_FILE", "storage/orders.json")

# Concurrency lock
order_lock = Lock()


# LOAD / SAVE ORDERS

def load_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_orders(data):
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# CREATE ORDER

def create_order(data):

    if not data or "items" not in data or not isinstance(data["items"], list):
        return error_response("Invalid order request", "ORDER005", 400)

    if len(data["items"]) == 0:
        return error_response("Order must contain at least one item", "ORDER006", 400)

    with order_lock:

        orders = load_orders()
        total_amount = 0
        products_to_update = []

        # VALIDATE ALL ITEMS FIRST
        for item in data["items"]:

            product_id = item.get("product_id")
            quantity = item.get("quantity")

            if not product_id or not quantity or quantity <= 0:
                return error_response("Invalid order item", "ORDER007", 400)

            product = Product.query.get(product_id)

            if not product:
                return error_response("Product not found", "PROD404", 404)

            if not product.is_active:
                return error_response("Inactive product", "ORDER008", 400)

            if product.stock_quantity < quantity:
                return error_response("Insufficient stock", "ORDER003", 400)

            total_amount += product.price * quantity
            products_to_update.append((product, quantity))

        # DEDUCT STOCK
        try:
            for product, quantity in products_to_update:
                product.stock_quantity -= quantity

            db.session.commit()

        except Exception:
            db.session.rollback()
            return error_response("Database error during order creation", "ORDER009", 500)

        #  CREATE ORDER
        order = {
            "order_id": str(uuid.uuid4()),
            "customer_name": data.get("customer_name"),
            "customer_email": data.get("customer_email"),
            "items": data["items"],
            "total_amount": total_amount,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }

        orders.append(order)
        save_orders(orders)

        return order


# UPDATE ORDER STATUS 

def update_order_status(order_id, new_status):

    valid_flow = {
        "pending": ["confirmed"],
        "confirmed": ["shipped"],
        "shipped": [],
        "cancelled": []
    }

    if not new_status:
        return error_response("Status required", "ORDER010", 400)

    orders = load_orders()

    for order in orders:

        if order["order_id"] == order_id:

            current_status = order["status"]

            if new_status not in valid_flow[current_status]:
                return error_response("Invalid status transition", "ORDER001", 400)

            order["status"] = new_status
            save_orders(orders)

            return {"message": "Order status updated successfully"}

    return error_response("Order not found", "ORDER404", 404)


# CANCEL ORDER

def cancel_order(order_id):

    with order_lock:

        orders = load_orders()

        for order in orders:

            if order["order_id"] == order_id:

                if order["status"] not in ["pending", "confirmed"]:
                    return error_response("Order cannot be cancelled", "ORDER002", 400)

                # Restore stock
                try:
                    for item in order["items"]:
                        product = Product.query.get(item["product_id"])

                        if product:
                            product.stock_quantity += item["quantity"]

                    db.session.commit()

                except Exception:
                    db.session.rollback()
                    return error_response("Database error during cancellation", "ORDER011", 500)

                order["status"] = "cancelled"
                save_orders(orders)

                return {"message": "Order cancelled successfully"}

        return error_response("Order not found", "ORDER404", 404)
