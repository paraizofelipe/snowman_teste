from snowman_teste.models import User, Authenticator, TourPoint, Category, session
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import ModelSchema


class AuthenticatorSchema(ModelSchema):
    class Meta:
        model = Authenticator
        sql_session = session


class CategorySchema(ModelSchema, Schema):
    class Meta:
        model = Category
        sql_session = session


class TourPointSchema(ModelSchema, Schema):
    class Meta:
        model = TourPoint
        category = fields.Nested(CategorySchema, many=True)
        sql_session = session


class UserSchema(ModelSchema):
    class Meta:
        model = User
        sql_session = session

