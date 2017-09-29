from snowman_teste.models import User, Authenticator, TourPoint, Category, Session
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class AuthenticatorSchema(ModelSchema):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, exclude=('user',))

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, exclude=('password',))

    authenticator = fields.Nested(AuthenticatorSchema, exclude=('salt',))

    class Meta:

        model = User
        sql_session = Session


