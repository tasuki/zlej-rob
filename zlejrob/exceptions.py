class OffTheBoardError(RuntimeError):
    pass

class UnexpectedHTTPStatusCode(IOError):
    pass

class GenerationLimitExceeded(RuntimeError):
    pass
