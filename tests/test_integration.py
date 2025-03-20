import unittest
from models.user import User
from models.product import Product
from models.database import db


class TestIntegration(unittest.TestCase):
    def setUp(self):
        db.get_collection("users").delete_many({})
        db.get_collection("products").delete_many({})
        db.get_collection("orders").delete_many({})
        db.get_collection("order_items").delete_many({})
        db.get_collection("payments").delete_many({})
        db.get_collection("shopping_carts").delete_many({})

    def test_user_places_order(self):
        user = User(0, "Test User", "testuser@example.com", "password123")
        user.register()

        product1 = Product(1, "Phone", 10000, 10)
        product2 = Product(2, "Laptop", 25000, 5)

        user.cart.add_item(product1, 1)
        user.cart.add_item(product2, 2)

        self.assertEqual(user.cart.get_total(), 60000)

        order = user.create_order()
        self.assertEqual(order.total_price, 60000)

        result = order.checkout()
        self.assertEqual(result, "Payment of 60000 UAH processed via credit_card")

        orders = user.view_orders()
        self.assertEqual(len(orders), 1)
        self.assertIn("Order #1001: 60000 UAH, Status: completed", orders)

        self.assertEqual(product1.stock, 9)
        self.assertEqual(product2.stock, 3)