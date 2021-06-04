from marshmallow import Schema, fields

class UsernameValidatorSchema(Schema):
    username = fields.String(required=True)



