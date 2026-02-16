from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import require_api_key
from app.services.order_service import (
    create_order,
    update_order_status,
    cancel_order,
    load_orders
)
from app.utils.error_handler import error_response

order_bp = Blueprint("order", __name__)


# CREATE ORDER
@order_bp.route("/api/v1/orders", methods=["POST"])
@require_api_key()
def place_order():

    result = create_order(request.json)

    return jsonify(result) if isinstance(result, dict) else result


# GET ALL ORDERS
@order_bp.route("/api/v1/orders")
@require_api_key()
def list_orders():
    return jsonify(load_orders())


# GET SINGLE ORDER
@order_bp.route("/api/v1/orders/<order_id>")
@require_api_key()
def get_order(order_id):

    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id:
            return jsonify(order)

    return error_response("Order not found", "ORDER404", 404)


# UPDATE STATUS
@order_bp.route("/api/v1/orders/<order_id>/status", methods=["PATCH"])
@require_api_key("admin")
def change_status(order_id):

    data = request.json

    if not data or "status" not in data:
        return error_response("Invalid status update", "ORDER007", 400)

    return update_order_status(order_id, data["status"])


# CANCEL ORDER
@order_bp.route("/api/v1/orders/<order_id>/cancel", methods=["POST"])
@require_api_key()
def cancel(order_id):
    return cancel_order(order_id)
