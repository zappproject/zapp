import os

DEBUG = False

ADMINS = frozenset([
    os.environ.get('ADMINEMAIL')
])
