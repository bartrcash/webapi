from marshmallow import Schema, fields

class ChangePasswordValidatorSchema(Schema):
    password_recovery_request_id = fields.String(required=True)
    new_password = fields.String(required=True)



