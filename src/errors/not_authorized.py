from errors.custom_error import CustomException
from flask_babel import gettext


class NotAuthorized (CustomException):

    status_code = 401

    def to_dict(self):
        return {'message': gettext('Not authorized')}
