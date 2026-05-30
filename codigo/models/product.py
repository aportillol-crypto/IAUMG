from config.database import db


class Product(db.Model):
    """Modelo de producto del catalogo."""

    __tablename__ = "productos"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    category = db.Column(db.String(50), nullable=True)

    def __init__(self, name: str, price: float, stock: int = 0, category: str = None):
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def is_available(self) -> bool:
        return self.stock > 0

    def reduce_stock(self, quantity: int):
        if quantity > self.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}, solicitado: {quantity}")
        self.stock -= quantity

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": float(self.price),
            "stock": self.stock,
            "category": self.category,
        }

    def __repr__(self):
        return f"<Product product_id={self.product_id} name={self.name}>"
