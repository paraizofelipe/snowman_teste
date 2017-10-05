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
from sqlalchemy import ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy_utils import ChoiceType

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
    name = Column("USER_NAME", String)
    email = Column("USER_EMAIL", String, unique=True, nullable=False)
    password = Column("USER_PASSWORD", String, nullable=False)

    authenticator_id = Column("USER_AUTH_ID", Integer, ForeignKey('TB_AUTH.ID'))
    authenticator = relationship("Authenticator", uselist=False, back_populates="user")

    list_tour_points = relationship("TourPoint", back_populates="user", lazy="subquery")

    def __init__(self, email, password):
        self.created_at = dt.datetime.now()
        self.email = email
        self.authenticator = Authenticator({'email': self.email})
        self.password = hash_password(password, self.authenticator.salt)


class TourPoint(Base):
    
    CATEGORY = [
        (u'museum', u'museum'),
        (u'park', u'park'),
        (u'restaurant', u'restaurant')
    ]
    
    __tablename__ = "TB_TOUR_POINT"
    
    id = Column("ID", Integer, primary_key=True)
    name = Column("POINT_NAME", String, unique=True)
    created_at = Column("CREATED_AT", DateTime)
    latitude = Column("POINT_LATITUDE", Float, nullable=False)
    longitude = Column("POINT_LONGITUDE", Float, nullable=False)
    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.ID'))
    user = relationship("User", uselist=False, back_populates="list_tour_points")
    category = Column(ChoiceType(CATEGORY), nullable=False)
    public = Column("POINT_PUBliC", Boolean, default=True)
    address = Column("POINT_ADDRESS", String)

    def __init__(self, name, latitude, longitude, public, category):
        self.name = name
        self.created_at = dt.datetime.now()
        self.category = category
        self.latitude = latitude
        self.longitude = longitude
        self.public = public
        geocode = gmaps.reverse_geocode((latitude, longitude))[0]
        self.address = geocode['formatted_address']
