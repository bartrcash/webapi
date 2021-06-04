from marshmallow import Schema, fields

class UserEmailValidatorSchema(Schema):
    email = fields.String(required=True)



