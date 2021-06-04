from marshmallow import Schema, fields

class UserPasswordValidatorSchema(Schema):
    currentPassword = fields.String(required=True)
    newPassword = fields.String(required=True)


