from datetime import datetime

from hyprfire_app.exceptions import TimestampException
from math import isinf

# This timestamp represents the start of the year 3000
MAX_TIMESTAMP = 32503680000


def convert_to_editcap_format(timestamp):
    try:
        start_timestamp = int(timestamp)
        validate_timestamp(start_timestamp)
        formatted_start = datetime.fromtimestamp(start_timestamp)

        return formatted_start
    except ValueError:
        raise TimestampException('Timestamp must be a number')
    except OverflowError:
        raise TimestampException('Timestamp cannot be larger than a 64 bit integer')


def validate_timestamp(timestamp):
    if timestamp < 0:
        raise TimestampException('Timestamp cannot be less than zero')

    if isinf(timestamp):
        raise TimestampException('Timestamp cannot be infinite')

    if timestamp >= MAX_TIMESTAMP:
        raise TimestampException('Timestamp must be before the year 3000')
