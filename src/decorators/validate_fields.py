# functools
import functools

# flask
from flask import request

# marshmallow
from marshmallow import ValidationError

# erros
from errors.bad_request import BadRequest


def validate_fields(schema, many):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                schema().load(request.get_json(), many=many)
                return func(*args, **kwargs)

            except ValidationError as err:
                raise BadRequest("Invalid input")
                # print(err.messages)

        return wrapper

    return decorator
