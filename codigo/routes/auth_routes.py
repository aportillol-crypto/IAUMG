from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/auth/login
    Body: {"email": str, "password": str}
    Retorna JWT token si las credenciales son validas.
    Valida email y password_hash via AuthService.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email y password son requeridos"}), 400

    try:
        token = AuthService.login(email=email, password=password)
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.route("/verify", methods=["GET"])
def verify_token():
    """
    GET /api/auth/verify
    Header: Authorization: Bearer <token>
    Verifica si el token es valido y retorna el user_id del payload.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token no proporcionado"}), 401

    token = auth_header.replace("Bearer ", "")
    try:
        payload = AuthService.verify_token(token)
        return jsonify({"valid": True, "user_id": payload["user_id"], "email": payload["email"]}), 200
    except ValueError as e:
        return jsonify({"valid": False, "error": str(e)}), 401
