class JSONError(ValueError):
    """Exception raised when there's an error with JSON encoding/decoding"""


class TimestampException(ValueError):
    """Exception raised for when a timestamp is invalid"""


class EditcapException(Exception):
    """Exception raised when there's a problem in running the editcap tool"""


class ConverterException(Exception):
    """Exception raised when there's an issue running the converters"""
    def __init__(self, message="Something went wrong"):
        self.message = message

    def __str__(self):
        return f'{self.message}'
