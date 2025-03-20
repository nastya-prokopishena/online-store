import unittest
from models.user import User
from models.database import db


class TestUser(unittest.TestCase):
    def setUp(self):
        print("Clearing users collection...")
        db.get_collection("users").delete_many({})
        user_count = db.get_collection("users").count_documents({})
        self.assertEqual(user_count, 0, "Database was not cleared properly")

        self.user = User(0, "Test User", "testuser@example.com", "password123")

    def test_register_success(self):
        result = self.user.register()
        self.assertEqual(result, "User Test User registered with email testuser@example.com")

    def test_register_existing_email(self):
        self.user.register()
        result = self.user.register()
        self.assertEqual(result, "User Test User already registered with email testuser@example.com")

    def test_login_success(self):
        self.user.register()
        result = self.user.login("testuser@example.com", "password123")
        self.assertEqual(result, "User Test User logged in successfully")

    def test_login_invalid_password(self):
        self.user.register()
        with self.assertRaises(ValueError):
            self.user.login("testuser@example.com", "wrongpassword")

    def test_login_invalid_email(self):
        self.user.register()
        with self.assertRaises(ValueError):
            self.user.login("wrongemail@example.com", "password123")