from collections import defaultdict
from flask import jsonify
from app.services.order_service import load_orders
from app.models.product_model import Product


# LOW STOCK REPORT

def low_stock(threshold):

    products = Product.query.filter(
        Product.stock_quantity < threshold,
        Product.is_active == True
    ).all()

    return jsonify([
        {
            "product_id": p.id,
            "name": p.name,
            "stock_quantity": p.stock_quantity
        }
        for p in products
    ])


#SALES SUMMARY REPORT

def sales_summary():

    orders = load_orders()

    total_revenue = 0
    product_counter = defaultdict(int)

    # PROCESS ORDERS
    for order in orders:

        # Ignore cancelled orders
        if order["status"] == "cancelled":
            continue

        total_revenue += order["total_amount"]

        for item in order["items"]:
            product_counter[item["product_id"]] += item["quantity"]

    # TOP 5 PRODUCTS
    top_products = sorted(
        product_counter.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # Enrich with product names
    top_products_enriched = []

    for product_id, qty in top_products:
        product = Product.query.get(product_id)

        top_products_enriched.append({
            "product_id": product_id,
            "name": product.name if product else "Unknown",
            "quantity_sold": qty
        })

    # FINAL RESPONSE
    return jsonify({
        "total_revenue": total_revenue,
        "order_count": len([o for o in orders if o["status"] != "cancelled"]),
        "top_products": top_products_enriched
    })
