class BaseCorreioException(Exception):
    pass


class UnknownError(BaseCorreioException):
    def __str__(self) -> str:
        return 'Unknown error'


class OrderNotDispatched(BaseCorreioException):
    def __str__(self) -> str:
        return 'Order not dispatched'


class InvalidTrackingCode(BaseCorreioException):
    def __str__(self) -> str:
        return 'Invalid tracking code'


class NoTrackingData(BaseCorreioException):
    def __str__(self) -> str:
        return 'No tracking data available'
