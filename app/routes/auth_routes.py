from flask import Blueprint, request, jsonify
from app.services.auth_service import generate_api_key
from app.utils.error_handler import error_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/v1/auth/keys", methods=["POST"])
def create_key():
    """
    Generate API Key
    Required Body:
    {
        "owner": "string",
        "role": "admin | viewer"
    }
    """

    data = request.json

    # Validate request body
    if not data:
        return error_response("Request body required", "AUTH004", 400)

    owner = data.get("owner")
    role = data.get("role")

    # Validate required fields
    if not owner or not role:
        return error_response("Owner and role required", "AUTH005", 400)

    # Validate role values
    if role not in ["admin", "viewer"]:
        return error_response("Invalid role", "AUTH006", 400)

    # Generate key
    key = generate_api_key(owner, role)

    return jsonify({
        "api_key": key,
        "message": "API key generated successfully"
    }), 201
