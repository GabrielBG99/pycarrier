class BaseCorreioException(Exception):
    pass


class UnknownError(BaseCorreioException):
    pass


class OrderNotDispatched(BaseCorreioException):
    pass


class InvalidTrackingCode(BaseCorreioException):
    pass


class NoTrackingData(BaseCorreioException):
    pass
