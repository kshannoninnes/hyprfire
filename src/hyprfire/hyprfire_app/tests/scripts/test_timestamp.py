from django.test import TestCase

from hyprfire_app.exceptions import TimestampException
from hyprfire_app.new_scripts.packet_manipulator import timestamp


class TimestampTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_zero_timestamp(self):
        """
        test_zero_timestamp

        A zero timestamp shouldn't throw any exceptions
        """
        timestamp.validate_timestamp(0)

    def test_invalid_timestamp_format(self):
        """
        test_invalid_timestamp_format

        A timestamp with an incorrect format (eg. a string) should raise a TimestampException
        """
        self.assertRaises(TimestampException, timestamp.convert_to_editcap_format, 'hello')

    def test_too_large_timestamp(self):
        """
        test_too_large_timestamp

        A timestamp that that is larger than 64 bit integer maximum should throw a TimestampException
        """
        # This integer is the epoch timestamp for 3000-01-01 00:00:00
        max_int = 32503680000

        self.assertRaises(TimestampException, timestamp.convert_to_editcap_format, max_int)

    def test_infinite_timestamp(self):
        """
        test_infinite_timestamp

        An infinite timestamp should raise a TimestampException
        """
        self.assertRaises(TimestampException, timestamp.validate_timestamp, float("inf"))

    def test_negative_start(self):
        """
        test_negative_start

        A negative start time should raise a TimestampException
        """
        self.assertRaises(TimestampException, timestamp.validate_timestamp, -1)
