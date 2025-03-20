import unittest
from models.order import Order
from models.product import Product
from models.database import db

class TestOrder(unittest.TestCase):
    def setUp(self):
        print("Clearing database for Order tests...")
        db.get_collection("orders").delete_many({})
        db.get_collection("order_items").delete_many({})
        db.get_collection("products").delete_many({})
        self.order = Order(1, 1)
        self.product = Product(1, "Test Product", 1000, 10)

    def test_add_product(self):
        self.order.add_product(self.product, 2)
        self.assertEqual(len(self.order.products), 1)
        self.assertEqual(self.order.total_price, 2000)
        updated_product = Product.find_by_id(1)
        self.assertEqual(updated_product.stock, 8)

    def test_remove_product(self):
        self.order.add_product(self.product, 2)
        self.order.remove_product(1)
        self.assertEqual(len(self.order.products), 0)
        self.assertEqual(self.order.total_price, 0)
        updated_product = Product.find_by_id(1)
        self.assertEqual(updated_product.stock, 10)

    def test_checkout_empty_order(self):
        with self.assertRaises(ValueError):
            self.order.checkout()