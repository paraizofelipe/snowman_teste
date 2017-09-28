import os
import jwt
import hashlib
import datetime as dt
from snowman_teste.utils import hash_password
from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import ForeignKey, Integer, String, DateTime


engine = create_engine("sqlite:///snowman.db", echo=False)
Session = scoped_session(sessionmaker(bind=engine))
# data_base = session()
Base = declarative_base(engine)


class Authenticator(Base):

    __tablename__ = "TB_AUTH"

    id = Column("ID", Integer, primary_key=True)
    api_token = Column("API_TOKEN", String)
    salt = Column("SALT", String)

    user = relationship("User", back_populates="authenticator")

    def __init__(self, payload=None):
        self.api_token = jwt.encode(payload=payload, key="serial-do-windows-xp", algorithm='HS256')
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

    def __init__(self, name: str, email: str, password: str):
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

    def __init__(self, name: str):
        self.name = name


class TourPoint(Base):

    __tablename__ = "TB_TOUR_POINT"

    id = Column("ID", Integer, primary_key=True)
    name = Column("POINT_NAME", String)
    created_at = Column("CREATED_AT", DateTime)
    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.ID'), nullable=True)

    category_id = Column("POINT_CATEGORY_ID", Integer, ForeignKey('TB_CATEGORY.ID'), nullable=True)
    category = relationship("Category", uselist=False, back_populates="tour_point")

    def __init__(self, name: str, user_id: int, category: Category):
        self.name = name
        self.created_at = dt.datetime.now()
        self.category = category
        self.user_id = user_id

# restaurante = Category(name='Restaurante')
# mouseu = Category(name='Mouseu')
#
# session.add(restaurante)
# session.add(mouseu)
# session.commit()
#
# user1 = User(name='Teste01', email='teste01@teste.com', password='1234')
# user2 = User(name='Teste02', email='teste02@teste.com', password='4321')
#
# session.add(user1)
# session.add(user2)
# session.commit()
#
# tour_point1 = TourPoint(name='Aqui', user_id=user1.id, category=restaurante)
# tour_point2 = TourPoint(name='Ali', user_id=user2.id, category=mouseu)
#
# session.add(tour_point1)
# session.add(tour_point2)
# session.commit()



