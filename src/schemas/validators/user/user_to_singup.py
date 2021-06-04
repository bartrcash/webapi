from marshmallow import Schema, fields
from ma import ma
from models.production.user import UserModel

class UserToSignupSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

class UserToSignupValidatorSchema(Schema):
    token = fields.String(required=True)
    user = fields.Nested(nested=UserToSignupSchema)


