from errors.custom_error import CustomException


class BadRequest (CustomException):

    status_code = 400

    def get_message(self):
        return self.message
