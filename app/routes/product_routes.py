from flask import Blueprint, request, jsonify
from app.models.product_model import Product
from app.db import db
from app.middleware.auth_middleware import require_api_key
from app.utils.error_handler import error_response
from threading import Lock

product_bp = Blueprint("product", __name__)
stock_lock = Lock()


# CREATE PRODUCT

@product_bp.route("/api/v1/products", methods=["POST"])
@require_api_key("admin")
def create_product():

    data = request.json

    if not data:
        return error_response("Invalid product data", "PROD003", 400)

    try:
        product = Product(**data)
        db.session.add(product)
        db.session.commit()

    except Exception:
        db.session.rollback()
        return error_response("Invalid product data", "PROD003", 400)

    return jsonify({"message": "Product created successfully"}), 201


# LIST PRODUCTS

@product_bp.route("/api/v1/products", methods=["GET"])
@require_api_key()
def list_products():

    query = Product.query.filter_by(is_active=True)

    search = request.args.get("search")

    # FULL TEXT SEARCH (PDF REQUIREMENT)
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.description.ilike(f"%{search}%")) |
            (Product.sku.ilike(f"%{search}%"))
        )

    products = query.all()

    return jsonify([
        {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock_quantity": p.stock_quantity,
            "category": p.category
        }
        for p in products
    ])


# GET SINGLE PRODUCT

@product_bp.route("/api/v1/products/<int:product_id>", methods=["GET"])
@require_api_key()
def get_product(product_id):

    product = Product.query.get(product_id)

    if not product or not product.is_active:
        return error_response("Product not found", "PROD404", 404)

    return jsonify({
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock_quantity": product.stock_quantity,
        "category": product.category
    })


# UPDATE PRODUCT 

@product_bp.route("/api/v1/products/<int:product_id>", methods=["PUT"])
@require_api_key("admin")
def update_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return error_response("Product not found", "PROD404", 404)

    data = request.json

    if not data:
        return error_response("Invalid product data", "PROD003", 400)

    try:
        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()

    except Exception:
        db.session.rollback()
        return error_response("Invalid product update", "PROD004", 400)

    return jsonify({"message": "Product updated successfully"})


# SOFT DELETE 

@product_bp.route("/api/v1/products/<int:product_id>", methods=["DELETE"])
@require_api_key("admin")
def delete_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return error_response("Product not found", "PROD404", 404)

    product.is_active = False
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"})


# ADJUST STOCK 

@product_bp.route("/api/v1/products/<int:product_id>/stock", methods=["PATCH"])
@require_api_key("admin")
def adjust_stock(product_id):

    data = request.json

    if not data or "adjust" not in data:
        return error_response("Invalid stock adjustment", "PROD005", 400)

    adjust_value = data["adjust"]

    with stock_lock:

        product = Product.query.get(product_id)

        if not product:
            return error_response("Product not found", "PROD404", 404)

        product.stock_quantity += adjust_value

        if product.stock_quantity < 0:
            return error_response("Stock cannot be negative", "PROD002", 400)

        db.session.commit()

    return jsonify({
        "product_id": product.id,
        "stock_quantity": product.stock_quantity
    })
