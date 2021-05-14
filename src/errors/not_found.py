from errors.custom_error import CustomException
from flask_babel import gettext


class NotFoundError (CustomException):

    status_code = 404

    def to_dict(self):
        return {'message': gettext('Not found')}
