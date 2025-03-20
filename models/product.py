from models.database import db

class Product:
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.save_to_db()

    def update_stock(self, quantity: int):
        if quantity < 0:
            raise ValueError("Stock cannot be negative")
        self.__stock = quantity
        db.get_collection("products").update_one(
            {"product_id": self.__product_id},
            {"$set": {"stock": self.__stock}}
        )

    def get_details(self):
        return f"Product ID: {self.__product_id}, Name: {self.__name}, Price: {self.__price}, Stock: {self.__stock}"

    def save_to_db(self):
        product_data = {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }
        db.get_collection("products").update_one(
            {"product_id": self.__product_id},
            {"$set": product_data},
            upsert=True
        )

    @staticmethod
    def find_by_id(product_id: int):
        product_data = db.get_collection("products").find_one({"product_id": product_id})
        if not product_data:
            return None
        return Product(
            product_data["product_id"],
            product_data["name"],
            product_data["price"],
            product_data["stock"]
        )

    @property
    def product_id(self):
        return self.__product_id

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock