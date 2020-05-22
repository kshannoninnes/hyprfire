from datetime import datetime

from hyprfire_app.utils.validation import validate_timestamp


def convert_to_editcap_format(timestamp):
    """
    convert_to_editcap_format

    Convert a timestamp into a format suitable for editcap

    Parameters
    timestamp: an integer representing an epoch timestamp

    Return
    A datetime representation of the timestamp in the format YYYY-MM-DD hh:mm:ss
    """

    validate_timestamp(timestamp)
    ts_seconds = int(timestamp)
    formatted_start = datetime.fromtimestamp(ts_seconds)

    return formatted_start


def timestamps_equal(first, second):
    """
    timestamps_equal

    Check if two timestamps are equal to a nanosecond precision

    Parameters
    first: the first timestamp
    second: the second timestamp

    Return
    True if the timestamps can be considered equal, False if not
    """
    eps = 0.000000001
    return abs(first - second) < eps

