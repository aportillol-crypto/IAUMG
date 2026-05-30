import os
import jwt
from datetime import datetime, timedelta
from services.user_service import UserService
from werkzeug.security import check_password_hash

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-production")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 24))


class AuthService:
    """Maneja autenticacion JWT de usuarios."""

    @staticmethod
    def login(email: str, password: str) -> str:
        """
        Autentica un usuario y retorna un token JWT.
        Busca al usuario por email, luego verifica el password_hash.
        """
        user = UserService.get_by_email(email)
        if not user:
            raise ValueError("Credenciales invalidas.")
        if not user.is_active:
            raise ValueError("La cuenta esta desactivada.")
        if not check_password_hash(user.password_hash, password):
            raise ValueError("Credenciales invalidas.")

        payload = {
            "user_id": user.user_id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_token(token: str) -> dict:
        """Decodifica y valida un JWT. Retorna el payload con user_id y email."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado.")
        except jwt.InvalidTokenError:
            raise ValueError("Token invalido.")

    @staticmethod
    def get_user_from_token(token: str):
        """Obtiene el objeto User a partir de un token JWT valido."""
        payload = AuthService.verify_token(token)
        user_id = payload.get("user_id")
        return UserService.get_by_id(user_id)
