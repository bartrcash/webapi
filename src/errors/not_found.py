from errors.custom_error import CustomException


class NotFoundError (CustomException):

    status_code = 404

    def get_message(self):
        return "Not fonud"
