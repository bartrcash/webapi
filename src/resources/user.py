# datetime
import datetime

# flask
from flask_restful import Resource
from flask import request

# models
from models.production.user import UserModel
from models.production.confirmation import ConfirmationModel
from models.production.password_recovery_request import PasswordRecoveryRequestModel

# schemas
from schemas.production.user import UserSchema

# schema validators
from schemas.validators.user.username import UsernameValidatorSchema
from schemas.validators.user.user_to_signin import UserToSigninValidatorSchema
from schemas.validators.user.user_email import UserEmailValidatorSchema
from schemas.validators.user.user_password import UserPasswordValidatorSchema
from schemas.validators.user.user_recovery_password_request import (
    UserRecoveryPasswordRequestValidatorSchema,
)
from schemas.validators.user.user_to_singup import UserToSignupValidatorSchema

# passlib
from passlib.hash import pbkdf2_sha256

# erros
from errors.bad_request import BadRequest
from errors.not_found import NotFoundError

# jwt
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_access_cookies,
    unset_refresh_cookies
)

# flask
from flask import request
from flask.helpers import make_response

# decorators
from decorators.validate_fields import validate_fields
from decorators.validate_recaptcha import validate_recaptcha


user_schema = UserSchema()
custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)


# method to sign in
class UserSignin(Resource):
    @validate_fields(schema=UserToSigninValidatorSchema, many=False)
    # @validate_recaptcha()
    def post(self):

        # get user data
        user = request.get_json()["user"]
        user_email = user.get("email")
        user_password = user.get("password")

        # find user by email
        userFound = UserModel.find_by_email(user_email)

        # compare passwords
        if userFound and custom_pbkdf2.verify(user_password, userFound.password):

            # create token
            access_token = create_access_token(
                identity=userFound.id, expires_delta=False, fresh=True
            )

            # create refresh token
            refresh_token = create_refresh_token(userFound.id)

            resp = make_response(
                {
                    "user": {
                        "id": userFound.id,
                        "username": userFound.username,
                        "email": userFound.email,
                    }
                }
            )
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)

            return resp

        raise BadRequest("Invalid credentials")


# create new user
class UserRegister(Resource):
    @validate_fields(schema=UserToSignupValidatorSchema, many=False)
    @validate_recaptcha()
    def post(self):

        # create user model
        user_json = request.get_json().get("user")
        user = user_schema.load(user_json)

        # check email and userame
        if UserModel.find_by_username(user.username):
            raise BadRequest("A user with that username already exists")

        if UserModel.find_by_email(user.email):
            raise BadRequest("A user with that email already exists")

        # Hash the password
        hashed_pass = custom_pbkdf2.hash(user.password)
        user.password = hashed_pass

        # save user
        user.save_to_db()

        # create confirmation
        # confirmation = ConfirmationModel(user.id)
        # confirmation.save_to_db()
        # user.send_confirmation_email()

        # create token
        access_token = create_access_token(
            identity=user.id, expires_delta=False, fresh=True
        )

        # create refresh token
        refresh_token = create_refresh_token(user.id)

        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            "message": "User created!",
        }, 201

        # except MailGunException as e:
        #     user.delete_from_db()
        #     return {"message": str(e)}, 500


# method to log out
class UserSignOut(Resource):
    def post(self):
        resp = make_response({"message": "Signed out"})
        
        unset_access_cookies(resp)
        unset_refresh_cookies(resp)

        return resp


# change username
class UserName(Resource):
    @classmethod
    @jwt_required()
    @validate_fields(schema=UsernameValidatorSchema, many=False)
    def put(cls):

        # get user id
        user_id = get_jwt_identity()

        # new username
        newusername = request.get_json()["username"]

        # check if username already exists
        if UserModel.find_by_username(newusername):
            raise BadRequest("Username already exists")

        else:
            # save new user name
            user = UserModel.find_by_id(user_id)
            user.username = newusername
            user.save_to_db()

        return {"message": "Username updated", "username": newusername}, 200


# change user email
class UserEmail(Resource):
    @classmethod
    @jwt_required()
    @validate_fields(schema=UserEmailValidatorSchema, many=False)
    def put(cls):

        # get user id
        user_id = get_jwt_identity()

        # get new email
        newemail = request.get_json()["email"]

        try:
            if UserModel.find_by_email(newemail):
                raise BadRequest("Email already exists")

            else:
                # save new email
                user = UserModel.find_by_id(user_id)
                user.email = newemail
                user.save_to_db()

                # send confirmation
                # confirmation = ConfirmationModel(user.id)
                # confirmation.save_to_db()
                # user.send_confirmation_email()

                return {"message": "Email updated", "email": newemail}, 200

        except:
            return {"message": "Error"}, 500


# change user password
class UserPassword(Resource):
    @classmethod
    @jwt_required()
    @validate_fields(schema=UserPasswordValidatorSchema, many=False)
    def put(cls):

        # get user id
        user_id = get_jwt_identity()

        # get current password
        currentPassword = request.get_json()["currentPassword"]

        # get new password
        newPassword = request.get_json()["newPassword"]

        # find user
        user = UserModel.find_by_id(user_id)

        # check if curent password provided is valid
        if custom_pbkdf2.verify(currentPassword, user.password):

            # hash and update password
            newHashedPassword = custom_pbkdf2.hash(newPassword)
            user.password = newHashedPassword
            user.save_to_db()

            return {"message": "Password updated"}, 200

        else:
            raise BadRequest("Incorrect password")


# recover password
class PasswordRecoveryRequest(Resource):
    @classmethod
    @validate_fields(schema=UserRecoveryPasswordRequestValidatorSchema, many=False)
    def post(cls):
        # get supplied email
        user_email = request.get_json()["email"]

        # find user
        userFound = UserModel.find_by_email(user_email)

        if userFound:

            # create recover_password_request
            password_recovery_request = PasswordRecoveryRequestModel(
                user_id=userFound.id
            )
            password_recovery_request.save_to_db()

            # link = request.host_url[:-1] + url_for(
            # "recover_password_request", confirmation_id=self.most_recent_confirmation.id
            # )

            # recover_password_request.send_email()

            # send email
            # userFound.send_notification_email(
            #     f"You new password is {new_password}")

            return {"message": password_recovery_request.id}, 200
        else:
            raise NotFoundError()


# method to resend a confirmation in case the user didn't get the email
class UserConfirmation(Resource):
    @classmethod
    def post(cls):

        # get user data
        user_email = request.get_json()["userEmail"]

        # find user by email
        user = UserModel.find_by_email(user_email)

        if not user:
            raise NotFoundError()

        # get latest confirmation
        confirmation = user.most_recent_confirmation

        if confirmation:
            if confirmation.confirmed:
                return {"message": "Already confirmed"}, 400

            confirmation.force_to_expire()

        # create new confirmation
        new_confirmation = ConfirmationModel(user.id)
        new_confirmation.save_to_db()

        # send confirmation to email
        # user.send_confirmation_email()

        return {"message": "Confirmation email was sent"}, 200

        # except MailGunException as e:
        #     return {"message": str(e)}, 500


# method to create a NOT fresh token
class TokenRefresh(Resource):
    @jwt_required
    def post(self):

        # get use id
        current_user = get_jwt_identity()

        # create new token
        new_token = create_access_token(
            identity=current_user, fresh=False, expires_delta=timedelta
        )

        expiration = datetime.datetime.now() + timedelta

        # return no fresh token
        return {"access_token": new_token, "expiration": expiration.isoformat()}, 200
