from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.user import User
from services.user_service import UserService
from config.database import db


class OrderService:
    """Logica de negocio para gestion de ordenes."""

    @staticmethod
    def create_order(user_id: int, items: list[dict]) -> Order:
        """
        Crea una nueva orden para un usuario.
        items: [{"product_id": int, "quantity": int}, ...]

        Reglas de negocio:
        - El usuario debe existir y estar activo (is_active=True).
        - Cada producto debe tener stock suficiente.
        - El total se calcula automaticamente.
        """
        user = UserService.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario user_id={user_id} no encontrado.")
        if not user.is_active:
            raise ValueError(f"El usuario user_id={user_id} esta desactivado.")

        total = 0.0
        order_items = []

        for item_data in items:
            product = db.session.query(Product).filter(
                Product.product_id == item_data["product_id"]
            ).first()

            if not product:
                raise ValueError(f"Producto product_id={item_data['product_id']} no encontrado.")
            if not product.is_available():
                raise ValueError(f"Producto '{product.name}' sin stock.")

            quantity = item_data["quantity"]
            product.reduce_stock(quantity)
            subtotal = float(product.price) * quantity
            total += subtotal

            order_items.append(OrderItem(
                product_id=product.product_id,
                quantity=quantity,
                unit_price=product.price,
            ))

        order = Order(user_id=user_id, total=total)
        db.session.add(order)
        db.session.flush()  # Para obtener order_id antes del commit

        for oi in order_items:
            oi.order_id = order.order_id
            db.session.add(oi)

        db.session.commit()
        return order

    @staticmethod
    def cancel_order(order_id: int, requesting_user_id: int) -> Order:
        """
        Cancela una orden.
        Regla de negocio: solo el dueno (user_id) puede cancelar su propia orden.
        """
        order = db.session.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise ValueError(f"Orden order_id={order_id} no encontrada.")
        if order.user_id != requesting_user_id:
            raise PermissionError("No tienes permiso para cancelar esta orden.")
        order.cancel()
        db.session.commit()
        return order

    @staticmethod
    def get_by_user(user_id: int) -> list:
        return db.session.query(Order).filter(Order.user_id == user_id).all()
