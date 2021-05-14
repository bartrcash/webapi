from marshmallow import pre_dump
from ma import ma
from models.production.user import UserModel

class UserSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password", )
        dump_only = ("id", "confirmation")
        load_instance= True

        @pre_dump
        def _pre_dump(self, user: UserModel):
            user.confirmation = [user.most_recent_confirmation]
            return user
