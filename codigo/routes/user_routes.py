from flask import Blueprint, request, jsonify
from services.user_service import UserService
from services.auth_service import AuthService
from routes.middleware import require_auth

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.route("/register", methods=["POST"])
def register():
    """POST /api/users/register — Registra un nuevo usuario."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password:
        return jsonify({"error": "email y password son requeridos"}), 400

    try:
        user = UserService.create(email=email, password=password, full_name=full_name)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@user_bp.route("/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id: int):
    """GET /api/users/<user_id> — Obtiene datos de un usuario por user_id."""
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"error": f"Usuario user_id={user_id} no encontrado"}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route("/<int:user_id>/email", methods=["PATCH"])
@require_auth
def update_email(user_id: int):
    """PATCH /api/users/<user_id>/email — Actualiza el email de un usuario."""
    data = request.get_json()
    new_email = data.get("email")
    if not new_email:
        return jsonify({"error": "El campo 'email' es requerido"}), 400

    try:
        user = UserService.update_email(user_id=user_id, new_email=new_email)
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/<int:user_id>/deactivate", methods=["POST"])
@require_auth
def deactivate_user(user_id: int):
    """POST /api/users/<user_id>/deactivate — Desactiva la cuenta."""
    try:
        user = UserService.deactivate(user_id=user_id)
        return jsonify({"message": f"Usuario user_id={user_id} desactivado", "user": user.to_dict()}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@user_bp.route("/<int:user_id>/orders", methods=["GET"])
@require_auth
def get_user_orders(user_id: int):
    """GET /api/users/<user_id>/orders — Retorna las ordenes del usuario."""
    orders = UserService.get_orders(user_id=user_id)
    return jsonify([o.to_dict() for o in orders]), 200
