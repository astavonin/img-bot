class TooManyRequests(RuntimeError):
    pass


class InternalHttpError(RuntimeError):
    pass


class InvalidCredentials(RuntimeError):
    pass


class UnableToParse(RuntimeError):
    pass
