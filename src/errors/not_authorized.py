from errors.custom_error import CustomException


class NotAuthorized (CustomException):

    status_code = 401

    def get_message(self):
        return "Not authorized"
