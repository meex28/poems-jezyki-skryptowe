# exception used in unauthorized requests
class Unauthorized(Exception):
    def __init__(self, message):
        self.message = message
