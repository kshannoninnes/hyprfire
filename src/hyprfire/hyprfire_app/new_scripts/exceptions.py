class PacketsNotFoundError(ValueError):
    """Exception raised when there are no packets found"""


class TimestampError(ValueError):
    """Exception raised when there is an error with a provided timestamp"""
