from models.database import db
from models.product import Product


class OrderItem:
    def __init__(self, order_item_id: int, order_id: int, product_id: int, quantity: int):
        self.__order_item_id = order_item_id
        self.__order_id = order_id
        self.__product_id = product_id
        self.__quantity = quantity
        self.__product = Product.find_by_id(product_id)
        if not self.__product:
            raise ValueError(f"Product with ID {product_id} not found")
        self.save_to_db()

    def get_subtotal(self):
        return self.__product.price * self.__quantity

    def save_to_db(self):
        order_item_data = {
            "order_item_id": self.__order_item_id,
            "order_id": self.__order_id,
            "product_id": self.__product_id,
            "quantity": self.__quantity
        }
        db.get_collection("order_items").update_one(
            {"order_item_id": self.__order_item_id},
            {"$set": order_item_data},
            upsert=True
        )

    @staticmethod
    def find_by_order_id(order_id: int):
        items = db.get_collection("order_items").find({"order_id": order_id})
        return [OrderItem(
            item["order_item_id"],
            item["order_id"],
            item["product_id"],
            item["quantity"]
        ) for item in items]

    @property
    def product_id(self):
        return self.__product_id

    @property
    def quantity(self):
        return self.__quantity

    @property
    def product(self):
        return self.__product
