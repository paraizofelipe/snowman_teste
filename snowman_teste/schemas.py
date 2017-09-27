from marshmallow import Schema, fields


class AuthenticatorSchema(Schema):
    token_id = fields.Str()
    salt = fields.Str()


class TourPointSchema(Schema):
    created_at = fields.DateTime()
    distance = fields.Int()


class UserSchema(Schema):
    created_at = fields.DateTime()
    username = fields.Str()
    password = fields.Str()
    authenticator = fields.Nested(AuthenticatorSchema, many=False)
    tour_points = fields.Nested(TourPointSchema, many=True)
