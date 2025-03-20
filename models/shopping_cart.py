from models.database import db
from models.product import Product

class ShoppingCart:
    def __init__(self, user_id: int):
        self.__user_id = user_id
        self.__items = self.load_items_from_db()

    def add_item(self, product, quantity: int):
        if product.stock < quantity:
            raise ValueError("Not enough stock available")
        for item in self.__items:
            if item["product_id"] == product.product_id:
                item["quantity"] += quantity
                product.update_stock(product.stock - quantity)
                self.save_to_db()
                return
        self.__items.append({"product_id": product.product_id, "quantity": quantity})
        product.update_stock(product.stock - quantity)
        self.save_to_db()

    def remove_item(self, product_id: int):
        product = Product.find_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        for item in self.__items:
            if item["product_id"] == product_id:
                product.update_stock(product.stock + item["quantity"])
                self.__items.remove(item)
                break
        self.save_to_db()

    def clear_cart(self):
        for item in self.__items:
            product = Product.find_by_id(item["product_id"])
            if product:
                product.update_stock(product.stock + item["quantity"])
        self.__items = []
        self.save_to_db()

    def get_total(self):
        total = 0
        for item in self.__items:
            product = Product.find_by_id(item["product_id"])
            if product:
                total += product.price * item["quantity"]
        return total

    def save_to_db(self):
        cart_data = {
            "user_id": self.__user_id,
            "items": self.__items
        }
        db.get_collection("shopping_carts").update_one(
            {"user_id": self.__user_id},
            {"$set": cart_data},
            upsert=True
        )

    def load_items_from_db(self):
        cart_data = db.get_collection("shopping_carts").find_one({"user_id": self.__user_id})
        return cart_data["items"] if cart_data and "items" in cart_data else []

    # Геттер
    @property
    def items(self):
        return self.__items