import os
from pymongo import MongoClient


class Database(object):
    URI = os.environ.get("MONGODB_URI")
    #URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()
        #Database.DATABASE = client['zappapp']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def delete_one(collection, query):
        Database.DATABASE[collection].delete_one(query)

