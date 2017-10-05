from hug.types import MarshmallowSchema
from hug.exceptions import InvalidTypeData
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

    # category = fields.Nested('self', only='value')

    class Meta:
        dump_only = ("category.value",)
        model = TourPoint
        sql_session = Session


class AlchemyMarshSchema(MarshmallowSchema):
    __slots__ = ("schema", )

    def __init__(self, schema, session):
        super().__init__(schema)
        self.schema = schema()
        self.session = session

    def __call__(self, value):
        value, errors = self.schema.loads(value) if isinstance(value, str) else self.schema.load(value, session=self.session)
        if errors:
            raise InvalidTypeData('Invalid {0} passed in'.format(self.schema.__class__.__name__), errors)
        return value