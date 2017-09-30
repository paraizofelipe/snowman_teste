from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema, field_for
from snowman_teste.models import Access, User, Authenticator, TourPoint, Category, Session


class AuthenticatorSchema(ModelSchema):

    class Meta:
        load_only = ('salt',)
        model = Authenticator
        sql_session = Session


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        sql_session = Session


class AccessSchema(ModelSchema):
    class Meta:
        model = Access
        sql_session = Session


class UserSchema(ModelSchema):

    authenticator = fields.Nested(AuthenticatorSchema, exclude=('user',))

    class Meta:
        load_only = ("password",)
        model = User
        sql_session = Session


class TourPointSchema(ModelSchema):

    category = fields.Nested(CategorySchema, only=('name',))
    user = fields.Nested(UserSchema, exclude=('authenticator',))
    access = fields.Nested(AccessSchema, only=('name',))

    class Meta:
        model = TourPoint
        sql_session = Session
