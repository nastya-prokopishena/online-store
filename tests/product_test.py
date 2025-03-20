import unittest
from models.product import Product
from models.database import db

class TestProduct(unittest.TestCase):
    def setUp(self):
        db.get_collection("products").delete_many({})
        self.product = Product(1, "Test Product", 1000, 10)

    def test_update_stock(self):
        self.product.update_stock(5)
        self.assertEqual(self.product.stock, 5)

    def test_update_stock_negative(self):
        with self.assertRaises(ValueError):
            self.product.update_stock(-1)

    def test_get_details(self):
        details = self.product.get_details()
        self.assertEqual(details, "Product ID: 1, Name: Test Product, Price: 1000, Stock: 10")