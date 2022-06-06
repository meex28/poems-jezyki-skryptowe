# exception used in unauthorized requests
class Unauthorized(Exception):
    def __init__(self, message):
        self.message = message


# exception used in in example DB errors
class InternalServerError(Exception):
    def __init__(self, message):
        self.message = message
