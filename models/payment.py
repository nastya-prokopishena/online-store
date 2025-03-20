from models.database import db

class Payment:
    def __init__(self, payment_id: int, order_id: int, amount: float, method: str):
        self.__payment_id = payment_id
        self.__order_id = order_id
        self.__amount = amount
        self.__method = method
        self.save_to_db()

    def process_payment(self):
        payment_status = "completed"
        db.get_collection("payments").update_one(
            {"payment_id": self.__payment_id},
            {"$set": {"status": payment_status}}
        )
        return f"Payment of {self.__amount} UAH processed via {self.__method}"

    def save_to_db(self):
        payment_data = {
            "payment_id": self.__payment_id,
            "order_id": self.__order_id,
            "amount": self.__amount,
            "method": self.__method,
            "status": "pending"
        }
        db.get_collection("payments").update_one(
            {"payment_id": self.__payment_id},
            {"$set": payment_data},
            upsert=True
        )