from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema, field_for
from snowman_teste.models import User, Authenticator, TourPoint, Session


class AuthenticatorSchema(ModelSchema):

    class Meta:
        exclude = ('id', 'user')
        load_only = ('salt',)
        model = Authenticator
        sql_session = Session


class UserSchema(ModelSchema):

    authenticator = fields.Nested(AuthenticatorSchema, exclude=('user',))

    class Meta:
        load_only = ("password",)
        model = User
        sql_session = Session


class TourPointSchema(ModelSchema):

    class Meta:
        model = TourPoint
        sql_session = Session
