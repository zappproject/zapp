import datetime
import uuid
from flask import session
from src.common.database import Database

from src.models.transaction import Transaction

__author__ = 'jslvtr'


class User(object):
    def __init__(self, username, password, address, balance, _id=None):
        self.username = username
        self.password = password
        self.address = address
        self.balance = balance
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one("users", {"username": username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(username, password):
        # Check whether a user's username matches the password they sent us
        user = User.get_by_username(username)
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @classmethod
    def register(cls, username, password, address, balance):
        user = cls.get_by_username(username)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(username, password, address, balance)
            new_user.save_to_mongo()
            session['username'] = username
            session['address'] = address
            return True
        else:
            # User exists :(
            return False

    @staticmethod
    def login(user_username):
        # login_valid has already been called
        session['username'] = user_username

    @staticmethod
    def logout():
        session['username'] = None

    def get_transactions(self, sender):
        return Transaction.find_transactions(sender)

    def get_address(self):
        return Blog.find_by_author_id(self._id)

    def new_transaction(self, recipient, amount, message, sent_received):
        transaction = Transaction(sender=self.username,
                                  recipient=recipient,
                                  amount=amount,
                                  message=message,
                                  sent_received=sent_received)
        transaction.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            "username": self.username,
            "_id": self._id,
            "password": self.password,
            "address": self.address,
            "balance": self.balance
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())

    def update_balance(self):
        Database.update('users', {"username": self.username}, self.json())
