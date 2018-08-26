import datetime
import uuid
from flask import session
from src.common.database import Database
from src.models.transaction import Transaction
from src.models.withdrawal import Withdrawal

__author__ = 'jslvtr'


class User(object):
    def __init__(self, username, password, address, priv_key, email, balance, contacts, default, _id=None):
        self.username = username
        self.password = password
        self.address = address
        self.priv_key = priv_key
        self.email = email if email is not None else "none"
        self.balance = balance
        self.contacts = contacts
        self.default = default
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def delete_withdrawal(withdrawal_id):
        return Withdrawal.delete_withdrawals(withdrawal_id)

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one("users", {"username": username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_address(cls, address):
        data = Database.find_one("users", {"address": address})
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
    def register(cls, username, password, address, priv_key, email, balance, contacts, default):
        user = cls.get_by_username(username)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(username, password, address, priv_key, email, balance, contacts, default)
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

    def get_transactions(self):
        return Transaction.find_transactions()

    def get_withdrawals(self):
        return Withdrawal.find_withdrawals()

    def get_contacts(self):
        return self.contacts

    def new_transaction(self, sender, recipient, amount, message, sent_received, date_received):
        transaction = Transaction(sender=sender,
                                  recipient=recipient,
                                  amount=amount,
                                  message=message,
                                  sent_received=sent_received,
                                  date_received=date_received
                                  )
        transaction.save_to_mongo()

    def new_withdrawal(self, withdrawer, amount, withdrawal_address):
        withdrawal = Withdrawal(withdrawer=withdrawer,
                                amount=amount,
                                withdrawal_address=withdrawal_address)
        withdrawal.save_to_mongo()


    def json(self):
        return {
            "username": self.username,
            "_id": self._id,
            "password": self.password,
            "address": self.address,
            "priv_key": self.priv_key,
            "email": self.email,
            "contacts": self.contacts,
            "balance": self.balance,
            "default": self.default

        }

    def save_to_mongo(self):
        Database.insert("users", self.json())

    def update_balance(self, balance):
        Database.update('users', {"username": self.username}, {'$set': {'balance': balance}})

    def update_address(self, address):
        Database.update('users', {"username": self.username}, {'$set': {'address': address}})

    def update_default(self, default):
        Database.update('users', {"username": self.username}, {'$set': {'default': default}})

    def update_contacts(self, contacts):
        Database.update('users', {"username": self.username}, {'$set': {'contacts': contacts}})
