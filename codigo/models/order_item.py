from config.database import db


class OrderItem(db.Model):
    """Item individual dentro de una orden."""

    __tablename__ = "orden_items"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("ordenes.order_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("productos.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    def subtotal(self) -> float:
        return float(self.unit_price) * self.quantity

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "subtotal": self.subtotal(),
        }
