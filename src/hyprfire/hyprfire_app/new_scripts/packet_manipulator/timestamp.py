from datetime import datetime

from hyprfire_app.exceptions import TimestampException
from math import isinf

# This timestamp represents 3000-01-01 00:00:00
MAX_TIMESTAMP = 32503680000


def convert_to_editcap_format(timestamp):
    """
    convert_to_editcap_format

    Convert a timestamp into a format suitable for editcap

    Parameters
    timestamp: an integer representing an epoch timestamp

    Return
    A datetime representation of the timestamp in the format YYYY-MM-DD hh:mm:ss
    """
    try:
        start_timestamp = int(timestamp)
        validate_timestamp(start_timestamp)
        formatted_start = datetime.fromtimestamp(start_timestamp)

        return formatted_start
    except ValueError:
        raise TimestampException('Timestamp must be a number')


def validate_timestamp(timestamp):
    """
    validate_timestamp

    A timestamp is valid if it represents a date between 1970-01-01 00:00:00 and 3000-01-01 00:00:00

    Parameters
    timestamp: an integer representing an epoch timestamp
    """
    if timestamp < 0:
        raise TimestampException('Timestamp cannot be less than zero')

    if isinf(timestamp):
        raise TimestampException('Timestamp cannot be infinite')

    if timestamp >= MAX_TIMESTAMP:
        raise TimestampException('Timestamp must be before the year 3000')
