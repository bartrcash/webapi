# flask
from flask import Blueprint
from flask_restful import Api

# resources
from resources.user import (
    UserRegister,
    UserSignin,
    UserSignOut,
    TokenRefresh,
    UserName,
    UserEmail,
    UserPassword,
    PasswordRecoveryRequest,
    UserConfirmation,
)

from resources.confirmation import ConfirmationByUser, Confirmation

from resources.password_recovery import PasswordRecoveryRequestStatus, ChangePassword

# Create bluepirnt
user_module = Blueprint("auth", __name__)
api = Api(user_module)

#### Add resources

# # # # # # # # user
# User signup
api.add_resource(UserRegister, "/signup")
# UserSignin
api.add_resource(UserSignin, "/signin")
# UserSignout
api.add_resource(UserSignOut, "/signout")


# UserName
api.add_resource(UserName, "/username")
# email
api.add_resource(UserEmail, "/email")
# password
api.add_resource(UserPassword, "/password")


# UserTokenRefresh
api.add_resource(TokenRefresh, "/tokenrefresh")

# recover password
# create password_recovery_request
api.add_resource(PasswordRecoveryRequest, "/passwordrecovery/request")

# get the status of the recover password request
api.add_resource(
    PasswordRecoveryRequestStatus,
    "/passwordrecovery/<string:password_recovery_request_id>/status",
)

# update the password from a recover password request
api.add_resource(ChangePassword, "/passwordrecovery/changepassword")

# # # # # confirmation
# user_confirm
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
# confirmation
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
# userconfirmationemail
api.add_resource(UserConfirmation, "/confirmationemail")
