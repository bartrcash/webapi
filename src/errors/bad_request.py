from errors.custom_error import CustomException
from flask_babel import gettext


class BadRequest (CustomException):

    status_code = 400

    def to_dict(self):
        return {'message': self.message}
