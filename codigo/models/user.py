from datetime import datetime
from config.database import db


class User(db.Model):
    """Modelo de usuario del sistema."""

    __tablename__ = "usuarios"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relacion uno-a-muchos con ordenes
    orders = db.relationship("Order", backref="user", lazy=True)

    def __init__(self, email: str, password_hash: str, full_name: str = None):
        self.email = email.lower().strip()
        self.password_hash = password_hash
        self.full_name = full_name

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }

    def deactivate(self):
        self.is_active = False

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
