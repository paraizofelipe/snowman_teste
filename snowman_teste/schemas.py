from marshmallow import Schema, fields


class AuthenticatorSchema(Schema):
        # id = fields.Integer()
        created_at = fields.DateTime()
        api_token = fields.String()
        salt = fields.String()


# class CategorySchema(Schema):
#         # id = fields.Integer()
#         created_at = fields.DateTime()
#         name = fields.String()


class TourPointSchema(Schema):
        # id = fields.Integer()
        created_at = fields.DateTime()
        name = fields.String(required=True)
        category = fields.String(required=True)


class UserSchema(Schema):
        # id = fields.Integer()
        created_at = fields.DateTime()
        name = fields.String(required=True)
        email = fields.Email(required=True)
        password = fields.String(required=True)
        authenticator = fields.Nested(AuthenticatorSchema)
        tour_poits = fields.Nested(TourPointSchema, many=True)

