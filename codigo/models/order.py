from datetime import datetime
from config.database import db


class Order(db.Model):
    """Modelo de orden de compra."""

    __tablename__ = "ordenes"

    ORDER_STATUS = ("pending", "processing", "completed", "cancelled")

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.user_id"), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relacion con items de la orden
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id: int, total: float):
        self.user_id = user_id
        self.total = total
        self.status = "pending"

    def cancel(self):
        if self.status == "completed":
            raise ValueError("No se puede cancelar una orden completada.")
        self.status = "cancelled"

    def complete(self):
        if self.status != "processing":
            raise ValueError("Solo se pueden completar ordenes en estado 'processing'.")
        self.status = "completed"

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "total": float(self.total),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Order order_id={self.order_id} user_id={self.user_id} status={self.status}>"
