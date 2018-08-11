import uuid
import datetime
import pymongo
from src.common.database import Database

__author__ = 'jslvtr'


class Withdrawal(object):
    def __init__(self, withdrawer, amount, withdrawal_address, _id=None):
        self.withdrawer = withdrawer
        self.amount = amount
        self.withdrawal_address = withdrawal_address
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='withdrawals',
                        data=self.json())

    def json(self):
        return {
            'withdrawer': self.withdrawer,
            'amount': self.amount,
            'withdrawal_address': self.withdrawal_address,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        transaction_data = Database.find_one(collection='withdrawal',
                                             query={'_id': id})
        return cls(**transaction_data)


    @classmethod
    def find_withdrawals(cls):
        return [cls(**withdrawal) for withdrawal in Database.find('withdrawals', {})]

    @staticmethod
    def delete_withdrawals(withdrawal_id):
        Database.delete_one('withdrawals', {"_id": withdrawal_id})
