# datetime
import datetime

# flask
from flask_restful import Resource
from flask import request

# models
from models.production.user import UserModel
from models.production.confirmation import ConfirmationModel

# schemas
from schemas.production.user import UserSchema

# passlib
from passlib.hash import pbkdf2_sha256

# traceback
import traceback

# from libs.mailgun import MailGunException
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                create_refresh_token,
                                jwt_required,
                                )

# uuid
from uuid import uuid4

# os
import os

user_schema = UserSchema()

timedelta = datetime.timedelta(minutes=int(
    os.environ.get('JWT_EXPIRATION_TIME', 5)))

custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)

# method to sign in


class UserSignin(Resource):
    def post(self):

        try:

            # get user data
            user_email = request.get_json()["email"]
            user_password = request.get_json()["password"]

            # find user by email
            # if userFound is None:
            userFound = UserModel.find_by_email(user_email)
            print("heyy")
            # compare passwords
            if userFound and custom_pbkdf2.verify(user_password, userFound.password):

                access_token = create_access_token(
                    identity=userFound.id, expires_delta=False, fresh=True)

                refresh_token = create_refresh_token(userFound.id)

                return {
                    "user": {
                        "user_id": userFound.id,
                        "username": userFound.username,
                        "access_token": access_token,
                        "refresh_token": refresh_token}
                }, 200

            return {"message":  "Invalid credentials"}, 404

        except Exception as e:
            print(e)
            return {"message": str(e)}, 500

# method to create new user


class UserRegister(Resource):
    def post(self):

        # create user model
        user_json = request.get_json()
        user = user_schema.load(user_json)

        try:

            # check email and userame
            if UserModel.find_by_username(user.username):
                return {"message": 'A user with that username already exists'}, 400

            if UserModel.find_by_email(user.email):
                return {"message":  'A user with that email already exists'}, 400

            # Hash the password
            hashed_pass = custom_pbkdf2.hash(user.password)
            user.password = hashed_pass

            # save user
            user.save_to_db()

            # create confirmation
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            # user.send_confirmation_email()

            # create token
            access_token = create_access_token(
                identity=user.id, expires_delta=False, fresh=True)

            refresh_token = create_refresh_token(user.id)

            return {
                "user": {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "message": 'User created!'
            }, 201

        # except MailGunException as e:
        #     user.delete_from_db()
        #     return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            user.delete_from_db()  # rollback
            return {"message": "Error when creating the user"}, 500

# method to log out


class UserLogout(Resource):
    @jwt_required
    def post(self):
        # jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        # BLACKLIST.add(jti)
        return {"message": "Logged out"}, 200


class User(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        pass
        # user_id = get_jwt_identity()
        # user = UserModel.find_by_id(user_id)
        # if not user:
        #     return {'message':  gettext('User not found')}, 404

        # return user_schema.dump(user), 200

    @classmethod
    @jwt_required
    def delete(cls):
        pass
        # user_id = get_jwt_identity()
        # user = UserModel.find_by_id(user_id)

        # if not user:
        #     return {'message': 'User not found'}, 404

        # user.delete_from_db()

        # return {'message':  gettext('User deleted')}, 200

# change username


class UserName(Resource):

    @classmethod
    @jwt_required
    def put(cls):

        # get user id
        user_id = get_jwt_identity()

        # new username
        newusername = request.get_json()["userName"]

        # check if username already exists
        if UserModel.find_by_username(newusername):
            return {"message": 'Username already exists'}, 400
        else:
            # save new user name
            user = UserModel.find_by_id(user_id)
            user.username = newusername
            user.save_to_db()

        return {"message":  'Username updated'}, 200

# change user email


class UserEmail(Resource):

    @classmethod
    @jwt_required
    def put(cls):

        # get user id
        user_id = get_jwt_identity()

        # get new email
        newemail = request.get_json()["userEmail"]

        try:
            if UserModel.find_by_email(newemail):
                return {"message": "Email already exists"}, 400
            else:
                # save new email
                user = UserModel.find_by_id(user_id)
                user.email = newemail
                user.save_to_db()

                # send confirmation
                confirmation = ConfirmationModel(user.id)
                confirmation.save_to_db()
                # user.send_confirmation_email()

                return {"message":  'Email updated'}, 200

        except:
            return {"message":  'Error'}, 500

# change user password


class UserPassword(Resource):

    @classmethod
    @jwt_required
    def put(cls):

        # get user id
        user_id = get_jwt_identity()

        # get current password
        currentPassword = request.get_json()["currentPassword"]

        # get new password
        newPassword = request.get_json()["newPassword"]

        # find user
        user = UserModel.find_by_id(user_id)

        if custom_pbkdf2.verify(currentPassword, user.password):

            newHashedPassword = custom_pbkdf2.hash(newPassword)
            user.password = newHashedPassword
            user.save_to_db()

            return {"message": "Password updated"}, 200

        else:
            return {"message": "Incorrect Password"}, 400

# reset password


class UserResetPassword (Resource):

    @classmethod
    def post(cls):
        # get supplied email
        user_email = request.get_json()["email"]

        # find user
        userFound = UserModel.find_by_email(user_email)

        if userFound:
            # change password
            new_password = uuid4().hex
            hashed_pass = custom_pbkdf2.hash(new_password)
            userFound.password = hashed_pass
            userFound.save_to_db()

            # send email
            # userFound.send_notification_email(
            #     f"You new password is {new_password}")

            return {"message": "We have sent you an email with your new password"}, 200
        else:
            return {'message': 'User not found'}, 404

# method to resend a confirmation in case the user dont get the email


class UserConfirmation(Resource):
    @classmethod
    def post(cls):

        # get user data
        user_email = request.get_json()["userEmail"]

        # find user by email
        user = UserModel.find_by_email(user_email)

        if not user:
            return {'message': 'User not found'}, 404

        try:
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

            return {"message":  'Confirmation email was sent'}, 200

        # except MailGunException as e:
        #     return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            return {"message":  'Error'}, 500


# method to create a NOT fresh token
class TokenRefresh(Resource):
    @jwt_required
    def post(self):

        # get use id
        current_user = get_jwt_identity()

        # create new token
        new_token = create_access_token(
            identity=current_user, fresh=False, expires_delta=timedelta)

        expiration = datetime.datetime.now() + timedelta

        # return no fresh token
        return {
            'access_token': new_token,
            "expiration": expiration.isoformat()
        }, 200
