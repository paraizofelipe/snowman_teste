import os
import jwt
import hashlib
import googlemaps
import datetime as dt
from snowman_teste.settings import CONFIG
from snowman_teste.utils import hash_password
from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import ForeignKey, Integer, String, DateTime, Float

from snowman_teste.settings import PATH

engine = create_engine("sqlite:///{}/snowman.db".format(PATH), echo=False)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base(engine)

print(engine.url)

gmaps = googlemaps.Client(key=CONFIG['api']['google_key'])


class Authenticator(Base):

    __tablename__ = "TB_AUTH"

    id = Column("ID", Integer, primary_key=True)
    api_token = Column("API_TOKEN", String)
    salt = Column("SALT", String)

    user = relationship("User", uselist=False, back_populates="authenticator")

    def __init__(self, payload=None):
        self.api_token = jwt.encode(payload=payload, key=CONFIG['auth']['secret'], algorithm='HS256')
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

    list_tour_points = relationship("TourPoint", back_populates="user", lazy="subquery")

    def __init__(self, name, email, password):
        self.created_at = dt.datetime.now()
        self.name = name
        self.email = email
        self.authenticator = Authenticator({'email': self.email})
        self.password = hash_password(password, self.authenticator.salt)


class Category(Base):

    __tablename__ = "TB_CATEGORY"

    id = Column("ID", Integer, primary_key=True)
    name = Column("CATEGORY_NAME", String, unique=True, nullable=False)

    tour_point = relationship("TourPoint", uselist=False, back_populates="category")

    def __init__(self, name):
        self.name = name


class Access(Base):

    __tablename__ = "TB_ACCESS"

    id = Column("ID", Integer, primary_key=True)
    name = Column("ACCESS_NAME", String, unique=True, nullable=False)

    tour_point = relationship("TourPoint", uselist=False, back_populates="access")

    def __init__(self, name):
        self.name = name


class TourPoint(Base):

    __tablename__ = "TB_TOUR_POINT"

    id = Column("ID", Integer, primary_key=True)
    name = Column("POINT_NAME", String)
    created_at = Column("CREATED_AT", DateTime)
    latitude = Column("POINT_LATITUDE", Float, nullable=False)
    longitude = Column("POINT_LONGITUDE", Float, nullable=False)
    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.ID'), nullable=False)
    user = relationship("User", uselist=False, back_populates="list_tour_points")
    category_id = Column("POINT_CATEGORY_ID", Integer, ForeignKey('TB_CATEGORY.ID'), nullable=False)
    category = relationship("Category", uselist=False, back_populates="tour_point")
    access_id = Column("POINT_ACESS", Integer, ForeignKey("TB_ACCESS.ID"), nullable=False)
    access = relationship("Access", uselist=False, back_populates="tour_point")
    address = Column("POINT_ADDRESS", String)

    def __init__(self, name, user_id, latitude, longitude, access_id, category_id):
        self.name = name
        self.created_at = dt.datetime.now()
        self.category_id = category_id
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude
        self.access_id = access_id
        geocode = gmaps.reverse_geocode((latitude, longitude))[0]
        self.address = geocode['formatted_address']
