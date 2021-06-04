from marshmallow import Schema, fields

class UserRecoveryPasswordRequestValidatorSchema(Schema):
    email = fields.String(required=True)



