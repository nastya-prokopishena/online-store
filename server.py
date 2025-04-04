from models.user import User
from models.admin import Admin
from models.product import Product
from models.database import db


def main():
    print("Clearing database...")
    user_count_before = db.get_collection("users").count_documents({})
    print(f"Users in database before clearing: {user_count_before}")

    result = db.get_collection("users").delete_many({})
    print(f"Deleted {result.deleted_count} users from the database")

    user_count_after = db.get_collection("users").count_documents({})
    print(f"Users in database after clearing: {user_count_after}")

    db.get_collection("products").delete_many({})
    db.get_collection("orders").delete_many({})
    db.get_collection("order_items").delete_many({})
    db.get_collection("payments").delete_many({})
    db.get_collection("shopping_carts").delete_many({})

    product1 = Product(1, "Phone", 10000, 10)
    product2 = Product(2, "Laptop", 25000, 5)

    user = User(0, "Anastasiia Prokopishena", "anastasiia.prokopishena@gmail.com", "password123")
    print(user.register())
    print(user.login("anastasiia.prokopishena@gmail.com", "password123"))

    user.cart.add_item(product1, 1)
    user.cart.add_item(product2, 2)
    print(f"Cart total: {user.cart.get_total()} UAH")

    order = user.create_order()
    print(f"Order created: {order.calculate_total()} UAH")

    print(order.checkout())

    print(user.view_orders())

    admin = Admin(0, "Valeria Schvalinska", "valeria.schvalinska@gmail.com", "admin123")
    print(admin.register())
    print(admin.login("valeria.schvalinska@gmail.com", "admin123"))

    product3 = Product(3, "Monitor", 15000, 8)
    print(admin.add_product(product3))

    print(admin.remove_product(3))

    print(admin.view_all_orders())


if __name__ == "__main__":
    main()