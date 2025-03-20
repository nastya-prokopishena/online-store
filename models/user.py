from models.database import db
from models.order import Order
from models.product import Product
from models.shopping_cart import ShoppingCart

class User:
    def __init__(self, user_id: int, name: str, email: str, password: str):
        self.__user_id = user_id if user_id else self.generate_user_id()
        self.__name = name
        self.__email = email
        self.__password = password
        self.__cart = ShoppingCart(self.__user_id)
        self.save_to_db()

    def generate_user_id(self):
        max_user = db.get_collection("users").find_one(sort=[("user_id", -1)])
        return (max_user["user_id"] + 1) if max_user else 1
    def register(self):
        existing_user = db.get_collection("users").find_one({"email": self.__email})
        if existing_user:
            print(f"User with email {self.__email} already exists, skipping registration")
            return f"User {self.__name} already registered with email {self.__email}"
        self.save_to_db()
        return f"User {self.__name} registered with email {self.__email}"

    def login(self, email: str, password: str):
        user_data = db.get_collection("users").find_one({"email": email})
        if not user_data or user_data["password"] != password:
            raise ValueError("Invalid email or password")
        return f"User {self.__name} logged in successfully"

    def view_orders(self):
        self.__orders = Order.find_by_user_id(self.__user_id)
        if not self.__orders:
            return "No orders found"
        return [f"Order #{order.order_id}: {order.total_price} UAH, Status: {order.status}" for order in self.__orders]

    def create_order(self):
        if not self.__cart.items:
            raise ValueError("Cart is empty")
        existing_orders = Order.find_by_user_id(self.__user_id)
        order = Order(order_id=self.__user_id * 1000 + len(existing_orders) + 1, user_id=self.__user_id)
        for item in self.__cart.items:
            product = Product.find_by_id(item["product_id"])
            if product:
                order.add_product(product, item["quantity"])
        self.__cart.clear_cart()
        return order

    def save_to_db(self):
        user_data = {
            "user_id": self.__user_id,
            "name": self.__name,
            "email": self.__email,
            "password": self.__password,
            "role": "user"
        }
        db.get_collection("users").update_one(
            {"user_id": self.__user_id},
            {"$set": user_data},
            upsert=True
        )

    @staticmethod
    def find_by_id(user_id: int):
        user_data = db.get_collection("users").find_one({"user_id": user_id})
        if not user_data:
            return None
        if user_data["role"] == "admin":
            from models.admin import Admin
            return Admin(
                user_data["user_id"],
                user_data["name"],
                user_data["email"],
                user_data["password"]
            )
        return User(
            user_data["user_id"],
            user_data["name"],
            user_data["email"],
            user_data["password"]
        )

    # Getters
    @property
    def user_id(self):
        return self.__user_id

    @property
    def cart(self):
        return self.__cart