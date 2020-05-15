from datetime import datetime

from hyprfire_app.exceptions import TimestampException
from math import isinf


def convert_to_editcap_format(start, end):
    # CAN THROW SOMETHING EXCEPTION?!
    start_timestamp = int(start)
    end_timestamp = int(end)

    # editcap can only capture packets with a 1s gap (eg. 16:47:24 - 16:47:24 will result in an empty file)
    if start_timestamp == end_timestamp:
        end_timestamp += 1

    # editcap requires timestamps in the format of "YYYY-MM-DD hh:mm:ss"
    formatted_start = datetime.fromtimestamp(start_timestamp)
    formatted_end = datetime.fromtimestamp(end_timestamp)

    return formatted_start, formatted_end


def validate_timestamp(timestamp):
    if timestamp < 0:
        raise TimestampException('Timestamp cannot be less than zero')

    if isinf(timestamp):
        raise TimestampException('Timestamp cannot be infinite')