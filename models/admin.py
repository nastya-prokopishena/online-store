from models.database import db
from models.user import User
from models.order import Order
from models.product import Product


class Admin(User):
    def __init__(self, admin_id: int, name: str, email: str, password: str):
        self.__admin_id = admin_id if admin_id else self.generate_user_id()
        super().__init__(self.__admin_id, name, email, password)

    def add_product(self, product: Product):
        product.save_to_db()
        return f"Product {product.get_details()} added by Admin"

    def remove_product(self, product_id: int):
        product = Product.find_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        db.get_collection("products").delete_one({"product_id": product_id})
        return f"Product with ID {product_id} removed by Admin"

    def view_all_orders(self):
        all_orders = Order.find_all()
        if not all_orders:
            return "No orders found"
        return [f"Order #{order.order_id}: {order.total_price} UAH, Status: {order.status}" for order in all_orders]

    def save_to_db(self):
        admin_data = {
            "user_id": self.__admin_id,
            "name": self._User__name,
            "email": self._User__email,
            "password": self._User__password,
            "role": "admin"
        }
        db.get_collection("users").update_one(
            {"user_id": self.__admin_id},
            {"$set": admin_data},
            upsert=True
        )
