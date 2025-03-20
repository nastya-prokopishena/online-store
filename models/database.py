from pymongo import MongoClient


class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["internet_shop"]

    def get_collection(self, collection_name):
        return self.db[collection_name]


db = Database()
