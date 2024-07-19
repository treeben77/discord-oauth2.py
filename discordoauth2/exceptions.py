class Exceptions:
    class BaseException(Exception):
        pass

    class HTTPException(BaseException):
        pass

    class RateLimited(HTTPException):
        def __init__(self, text, retry_after):
            self.retry_after = retry_after
            super().__init__(text)

    class Forbidden(HTTPException):
        pass


# Alias for compatibility with the old version, but class names should follow the CapitalizedWords convention
exceptions = Exceptions
