from models.user import User
from models.order import Order
from config.database import db
from config.cache import cache


class UserService:
    """Logica de negocio para gestion de usuarios."""

    @staticmethod
    def get_by_id(user_id: int) -> User:
        """Busca un usuario por su user_id. Usa cache Redis."""
        cache_key = f"user:{user_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        user = db.session.query(User).filter(User.user_id == user_id).first()
        if user:
            cache.set(cache_key, user, timeout=300)
        return user

    @staticmethod
    def get_by_email(email: str) -> User:
        """Busca un usuario por email (normalizado a minusculas)."""
        normalized_email = email.lower().strip()
        return db.session.query(User).filter(User.email == normalized_email).first()

    @staticmethod
    def create(email: str, password: str, full_name: str = None) -> User:
        """
        Crea un nuevo usuario.
        Regla de negocio: el email debe ser unico en el sistema.
        """
        if UserService.get_by_email(email):
            raise ValueError(f"Ya existe un usuario con el email: {email}")

        from werkzeug.security import generate_password_hash
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_email(user_id: int, new_email: str) -> User:
        """
        Actualiza el email de un usuario.
        Impacto: invalida el cache por user_id y valida unicidad.
        """
        user = UserService.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con user_id={user_id} no encontrado.")

        if UserService.get_by_email(new_email):
            raise ValueError(f"El email {new_email} ya esta en uso.")

        user.email = new_email.lower().strip()
        db.session.commit()

        # Invalidar cache
        cache.delete(f"user:{user_id}")
        return user

    @staticmethod
    def deactivate(user_id: int) -> User:
        """Desactiva la cuenta de un usuario. No elimina el registro."""
        user = UserService.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con user_id={user_id} no encontrado.")
        user.deactivate()
        db.session.commit()
        cache.delete(f"user:{user_id}")
        return user

    @staticmethod
    def get_orders(user_id: int) -> list:
        """Retorna todas las ordenes de un usuario dado su user_id."""
        return db.session.query(Order).filter(Order.user_id == user_id).all()

    @staticmethod
    def get_active_users() -> list:
        return db.session.query(User).filter(User.is_active == True).all()
