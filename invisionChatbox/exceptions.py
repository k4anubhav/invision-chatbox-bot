class APIException(Exception):
    def __init__(self):
        self.message = '!200 response from api'


class OpenConvException(Exception):
    def __init__(self):
        self.message = 'Error while opening conv non 200 response'


class OpenConvServerException(Exception):
    def __init__(self):
        self.message = 'Get error response on opening conv'
