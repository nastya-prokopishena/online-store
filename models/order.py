from models.database import db
from models.order_item import OrderItem
from models.payment import Payment
from models.product import Product


class Order:
    def __init__(self, order_id: int, user_id: int):
        self.__order_id = order_id
        self.__user_id = user_id
        self.__status = "pending"
        self.__total_price = 0.0
        self.__products = []
        self.__payment = None
        self.load_products_from_db()

    def add_product(self, product, quantity: int):
        if product.stock < quantity:
            raise ValueError("Not enough stock available")
        order_item = OrderItem(
            order_item_id=len(self.__products) + 1,
            order_id=self.__order_id,
            product_id=product.product_id,
            quantity=quantity
        )
        self.__products.append(order_item)
        product.update_stock(product.stock - quantity)
        self.calculate_total()
        self.save_to_db()

    def remove_product(self, product_id: int):
        for item in self.__products:
            if item.product_id == product_id:
                product = Product.find_by_id(product_id)
                if product:
                    product.update_stock(product.stock + item.quantity)
                self.__products.remove(item)
                break
        self.calculate_total()
        self.save_to_db()

    def calculate_total(self):
        self.__total_price = sum(item.get_subtotal() for item in self.__products)
        db.get_collection("orders").update_one(
            {"order_id": self.__order_id},
            {"$set": {"total_price": self.__total_price}}
        )
        return self.__total_price

    def checkout(self):
        if not self.__products:
            raise ValueError("Order is empty")
        self.__status = "completed"
        self.__payment = Payment(
            payment_id=self.__order_id,
            order_id=self.__order_id,
            amount=self.__total_price,
            method="credit_card"
        )
        self.save_to_db()
        return self.__payment.process_payment()

    def save_to_db(self):
        order_data = {
            "order_id": self.__order_id,
            "user_id": self.__user_id,
            "status": self.__status,
            "total_price": self.__total_price,
            "products": [{"order_item_id": item._OrderItem__order_item_id} for item in self.__products]
        }
        db.get_collection("orders").update_one(
            {"order_id": self.__order_id},
            {"$set": order_data},
            upsert=True
        )

    def load_products_from_db(self):
        order_data = db.get_collection("orders").find_one({"order_id": self.__order_id})
        if order_data and "products" in order_data:
            self.__products = OrderItem.find_by_order_id(self.__order_id)
            self.__status = order_data["status"]
            self.__total_price = order_data["total_price"]

    @staticmethod
    def find_by_user_id(user_id: int):
        orders = db.get_collection("orders").find({"user_id": user_id})
        return [Order(order["order_id"], order["user_id"]) for order in orders]

    @staticmethod
    def find_all():
        orders = db.get_collection("orders").find()
        return [Order(order["order_id"], order["user_id"]) for order in orders]

    @property
    def order_id(self):
        return self.__order_id

    @property
    def total_price(self):
        return self.__total_price

    @property
    def products(self):
        return self.__products

    @property
    def status(self):
        return self.__status
