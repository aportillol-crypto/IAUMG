from functools import wraps
from flask import request, jsonify, g
from services.auth_service import AuthService


def require_auth(f):
    """Decorador: valida JWT en el header Authorization antes de ejecutar la ruta."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Autenticacion requerida"}), 401
        token = auth_header.replace("Bearer ", "")
        try:
            user = AuthService.get_user_from_token(token)
            g.current_user = user
            g.current_user_id = user.user_id
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated
