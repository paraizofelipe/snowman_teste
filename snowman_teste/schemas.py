from snowman_teste.models import User, Authenticator, TourPoint, Category, Session
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class AuthenticatorSchema(ModelSchema):

    class Meta:
        model = Authenticator
        sql_session = Session


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        sql_session = Session


class TourPointSchema(ModelSchema):

    class Meta:
        model = TourPoint
        sql_session = Session


class UserSchema(ModelSchema):

    authenticator = fields.Nested(AuthenticatorSchema, exclude=('password', 'user'))

    class Meta:
        model = User
        sql_session = Session


