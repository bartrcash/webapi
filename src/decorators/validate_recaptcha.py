# functools
import functools

# flask
from flask import request

# erros
from errors.bad_request import BadRequest

# RecaptchaManager
from libs.recaptcha_manager import RecaptchaManager


def validate_recaptcha():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            token = request.get_json().get("token")

            result = RecaptchaManager.verify_recaptcha(token)

            if not result:
                raise BadRequest("Can't validate user ineraction")

            return func(*args, **kwargs)

        return wrapper

    return decorator
