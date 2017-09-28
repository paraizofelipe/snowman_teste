import os
import jwt
import hashlib
import datetime as dt
from snowman_teste.utils import hash_password


class Authenticator:

    def __init__(self, payload=None):
        self.api_token = jwt.encode(payload=payload, key="serial-do-windows-xp", algorithm='HS256')
        self.salt = hashlib.sha512(str(os.urandom(64)).encode('utf-8')).hexdigest()


class User:

    def __init__(self, name: str, email: str, password: str):
        self.created_at = dt.datetime.now()
        self.name = name
        self.email = email
        self.authenticator = Authenticator({'email': self.email, 'payload': 'pizza'})
        self.password = hash_password(password, self.authenticator.salt)


class TourPoint:

    def __init__(self, name: str, user: User, category: str):
        self.name = name
        self.created_at = dt.datetime.now()
        self.category = category
        self.user = user



