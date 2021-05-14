import abc

class CustomException(Exception, metaclass=abc.ABCMeta):

    status_code = 500

    def __init__(self, message=None):
        Exception.__init__(self)
        self.message = message

    @abc.abstractmethod
    def to_dict(self):
        pass
