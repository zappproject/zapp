import uuid

import pymongo

from src.common.database import Database

__author__ = 'jslvtr'


class Transaction(object):
    def __init__(self, sender, recipient, amount, message, sent_received, date_received, _id=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.message = message
        self.sent_received = sent_received
        self.date_received = date_received
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='transactions',
                        data=self.json())

    def json(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'message': self.message,
            'sent_received': self.sent_received,
            'date_received': self.date_received,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        transaction_data = Database.find_one(collection='transactions',
                                             query={'_id': id})
        return cls(**transaction_data)


    @classmethod
    def find_transactions(cls):
        return [cls(**transaction) for transaction in Database.find('transactions', {}).sort('date_received', pymongo.DESCENDING).limit(10)]
