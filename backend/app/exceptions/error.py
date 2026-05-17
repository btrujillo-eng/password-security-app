class EmailAlreadyExistsError(Exception):
    def __init__(self, message: str):
        self.message = message
        
class UserDoesNotExistsError(Exception):
    def __init__(self, message: str):
        self.message = message
        