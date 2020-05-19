from decimal import Decimal, InvalidOperation
from math import isinf
from pathlib import Path

from hyprfire_app.exceptions import TimestampException

MAX_TIMESTAMP = 32503680000


def validate_file_path(file_path):
    """
    validate_file_path

    A file path is valid if it points to an existing file

    Parameters
    file_path: a string representation of a file path

    Return
    The file path if it points to a valid file
    """
    path = Path(file_path)
    name = path.stem.lower()

    if not path.is_file() and not name.startswith('.'):
        raise FileNotFoundError('File Not Found.')

    return str(path)


def validate_timestamp(timestamp):
    """
    validate_timestamp

    A timestamp is valid if it represents a date between 1970-01-01 00:00:00 and 3000-01-01 00:00:00

    Parameters
    timestamp: a number representing an epoch timestamp

    Return
    A decimal representation of the original timestamp if it is valid
    """

    # Duh...
    try:
        timestamp = Decimal(timestamp)
    except InvalidOperation:
        raise TimestampException('Timestamp must be a number')

    # Also Duh...
    if isinf(timestamp):
        raise TimestampException('Timestamp cannot be infinite')

    # No such epoch timestamps before 0
    if timestamp < 0:
        raise TimestampException('Timestamp cannot be less than zero')

    # Prevent issues with overflows by passing in a massive number
    if timestamp >= MAX_TIMESTAMP:
        raise TimestampException('Timestamp must be before the year 3000')

    return timestamp
