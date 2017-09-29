import os
import jwt
import hashlib
import googlemaps
import datetime as dt
from snowman_teste.utils import hash_password, get_conf_key
from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import ForeignKey, Integer, String, DateTime, Float


engine = create_engine("sqlite:///snowman.db", echo=False)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base(engine)

gmaps = googlemaps.Client(key=get_conf_key('api')['google_key'])


class Authenticator(Base):

    __tablename__ = "TB_AUTH"

    id = Column("ID", Integer, primary_key=True)
    api_token = Column("API_TOKEN", String)
    salt = Column("SALT", String)

    user = relationship("User", back_populates="authenticator")

    def __init__(self, payload=None):
        self.api_token = jwt.encode(payload=payload, key=get_conf_key('auth')['secret'], algorithm='HS256')
        self.salt = hashlib.sha512(str(os.urandom(64)).encode('utf-8')).hexdigest()


class User(Base):

    __tablename__ = "TB_USER"

    id = Column("ID", Integer, primary_key=True)
    created_at = Column("CREATED_AT", DateTime)
    name = Column("USER_NAME", String, nullable=False)
    email = Column("USER_EMAIL", String, unique=True, nullable=False)
    password = Column("USER_PASSWORD", String, nullable=False)

    authenticator_id = Column("USER_AUTH_ID", Integer, ForeignKey('TB_AUTH.ID'))
    authenticator = relationship("Authenticator", uselist=False, back_populates="user")

    list_tour_points = relationship("TourPoint", backref='TB_USER', lazy="subquery")

    def __init__(self, name, email, password):
        self.created_at = dt.datetime.now()
        self.name = name
        self.email = email
        self.authenticator = Authenticator({'email': self.email, 'payload': 'pizza'})
        self.password = hash_password(password, self.authenticator.salt)


class Category(Base):

    __tablename__ = "TB_CATEGORY"

    id = Column("ID", Integer, primary_key=True)
    name = Column("CATEGORY_NAME", String, unique=True, nullable=False)

    tour_point = relationship("TourPoint", back_populates="category")

    def __init__(self, name):
        self.name = name


class TourPoint(Base):

    __tablename__ = "TB_TOUR_POINT"

    id = Column("ID", Integer, primary_key=True)
    name = Column("POINT_NAME", String)
    created_at = Column("CREATED_AT", DateTime)
    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.ID'), nullable=False)
    latitude = Column("POINT_LATITUDE", Float, nullable=False)
    longitude = Column("POINT_LONGITUDE", Float, nullable=False)
    category_id = Column("POINT_CATEGORY_ID", Integer, ForeignKey('TB_CATEGORY.ID'), nullable=False)
    category = relationship("Category", uselist=False, back_populates="tour_point")
    address = Column("POINT_ADDRESS", String)

    def __init__(self, name, user_id, latitude, longitude, category):
        self.name = name
        self.created_at = dt.datetime.now()
        self.category = category
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude
        geocode = gmaps.reverse_geocode((latitude, longitude))[0]
        self.address = geocode['formatted_address']
