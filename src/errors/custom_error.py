import abc

class CustomException(Exception, metaclass=abc.ABCMeta):

    def __init__(self, message=None):
        Exception.__init__(self)
        self.message = message

    
    @abc.abstractproperty
    def status_code(self):
        pass
   
    @abc.abstractmethod
    def get_message(self):
        pass
