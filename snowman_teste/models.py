import os
import jwt
import hashlib
import datetime as dt
from marshmallow import pprint
from snowman_teste import schemas
from snowman_teste.utils import hash_password
from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import ForeignKey, Integer, String, DateTime


engine = create_engine("sqlite:///snowman.db", echo=True)
session = sessionmaker()
session.configure(bind=engine)
db = session()

Base = declarative_base(engine)


class ModelPattern:

    def find_all(self):
        try:
            records = db.query(self.__class__).all()
            return records
        except Exception as error:
            raise error

    def find_by_id(self, id: int):
        try:
            record = db.query(self.__class__).filter_by(id=id).one()
            return record
        except Exception as error:
            raise error

    @staticmethod
    def create(obj):
        try:
            db.add(obj)
            db.commit()
        except Exception as error:
            raise error

    def delete(self, id: int):
        try:
            record = self.find_by_id(id)
            db.delete(record)
            db.commit()
        except Exception as error:
            raise error

    def update(self):
        pass


class Authenticator(Base, ModelPattern):

    __tablename__ = "TB_AUTH"

    id = Column("ID", Integer, primary_key=True)
    api_token = Column("API_TOKEN", String)
    salt = Column("SALT", String)

    user = relationship("User", back_populates="authenticator")

    def __init__(self, payload=None):
        self.api_token = jwt.encode(payload=payload, key="serial-do-windows-xp", algorithm='HS256')
        self.salt = hashlib.sha512(str(os.urandom(64)).encode('utf-8')).hexdigest()


class User(Base, ModelPattern):

    __tablename__ = "TB_USER"

    id = Column("ID", Integer, primary_key=True)
    created_at = Column("CREATED_AT", DateTime)
    name = Column("USER_NAME", String(100))
    email = Column("USER_EMAIL", String(100))
    password = Column("USER_PASSWORD", String(100))

    authenticator_id = Column("USER_AUTH_ID", Integer, ForeignKey('TB_AUTH.ID'))
    authenticator = relationship("Authenticator", uselist=False, back_populates="user")

    list_tour_points = relationship("TourPoint", backref='TB_USER', lazy="subquery")

    def __init__(self, name: str, email: str, password: str):
        self.created_at = dt.datetime.now()
        self.name = name
        self.email = email
        self.authenticator = Authenticator({'email': self.email, 'payload': 'pizza'})
        self.password = hash_password(password, self.authenticator.salt)


# class Category(Base, ModelPattern):
#
#     __tablename_ = "TB_CATEGORY"
#
#     id = Column("ID", Integer, primary_key=True)
#     name = Column("CATEGORY_NAME", String)


class TourPoint(Base, ModelPattern):

    __tablename__ = "TB_TOUR_POINT"

    id = Column("ID", Integer, primary_key=True)
    name = Column("POINT_NAME", String)
    # category = Column("POINT_CATEGORY")
    created_at = Column("CREATED_AT", DateTime)
    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.ID'))

    def __init__(self, name):
        self.name = name
        self.created_at = dt.datetime.now()


Base.metadata.create_all(engine)

user = User(name='Teste', email='teste@teste.com', password='1234')
# userT = User(name='Teste01', email='teste@teste.com', password='1234')
#
# aqui = TourPoint(name='Aqui do lado')
# ali = TourPoint(name='Ali do lado')
#
# user.list_tour_points.append(aqui)
# user.list_tour_points.append(ali)
# user.create(user)
#
# ali = TourPoint(name='Ali do lado')
# userT.list_tour_points.append(ali)
# userT.create(userT)

# schema = schemas.UserSchema()
# result = schema.dump(user)
