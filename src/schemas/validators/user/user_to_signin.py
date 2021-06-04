from marshmallow import Schema, fields

class UserToSigninSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

class UserToSigninValidatorSchema(Schema):
    token = fields.String(required=True)
    user = fields.Nested(nested=UserToSigninSchema)



