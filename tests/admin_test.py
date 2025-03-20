import unittest
from models.admin import Admin
from models.product import Product
from models.database import db


class TestAdmin(unittest.TestCase):
    def setUp(self):
        db.get_collection("users").delete_many({})
        db.get_collection("products").delete_many({})
        self.admin = Admin(0, "Test Admin", "testadmin@example.com", "admin123")

    def test_add_product(self):
        product = Product(1, "Test Product", 1000, 10)
        result = self.admin.add_product(product)
        self.assertEqual(result, "Product Product ID: 1, Name: Test Product, Price: 1000, Stock: 10 added by Admin")

    def test_remove_product(self):
        product = Product(1, "Test Product", 1000, 10)
        self.admin.add_product(product)
        result = self.admin.remove_product(1)
        self.assertEqual(result, "Product with ID 1 removed by Admin")
        self.assertIsNone(Product.find_by_id(1))

    def test_remove_nonexistent_product(self):
        with self.assertRaises(ValueError):
            self.admin.remove_product(999)
