# flask
from flask import request

# flask_restful
from flask_restful import Resource

# models
from models.production.password_recovery_request import PasswordRecoveryRequestModel
from models.production.user import UserModel

# erros
from errors.not_found import NotFoundError
from errors.bad_request import BadRequest


# schema validators
from schemas.validators.password_recovery.change_password import (
    ChangePasswordValidatorSchema,
)

# passlib
from passlib.hash import pbkdf2_sha256

# decorators
from decorators.validate_fields import validate_fields

custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)


# method return the stats of a password recovery request
class PasswordRecoveryRequestStatus(Resource):
    @classmethod
    def get(cls, password_recovery_request_id: str):

        # find password_recovery_request by id
        password_recovery_request = PasswordRecoveryRequestModel.find_by_id(
            password_recovery_request_id
        )

        # Nor found
        if password_recovery_request is None:
            raise NotFoundError()

        # Confirmartion expired
        if password_recovery_request.expired:
            raise BadRequest("Link expired")

        # Already confirmed
        if password_recovery_request.change_made:
            raise BadRequest("Link not available")

        return {"change_made": False}, 200


# change password from a password_Recovery_request
class ChangePassword(Resource):
    @classmethod
    @validate_fields(schema=ChangePasswordValidatorSchema, many=False)
    def post(cls):

        password_recovery_request_id = request.get_json()[
            "password_recovery_request_id"
        ]
        new_password = request.get_json()["new_password"]

        # find password_recovery_request by id
        password_recovery_request = PasswordRecoveryRequestModel.find_by_id(
            password_recovery_request_id
        )

        # Nor found
        if password_recovery_request is None:
            raise NotFoundError()

        # Already expired
        if password_recovery_request.expired:
            raise BadRequest("Link expired")

        # Password already changed
        if password_recovery_request.change_made:
            raise BadRequest("Link not available")

        userFound = UserModel.find_by_id(password_recovery_request.user_id)

        # Hash the password
        hashed_pass = custom_pbkdf2.hash(new_password)
        userFound.password = hashed_pass
        userFound.save_to_db()

        # update recover_password_request
        password_recovery_request.change_made = True
        password_recovery_request.save_to_db()

        return {"message": "Password changed"}, 200
