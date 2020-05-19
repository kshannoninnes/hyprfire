from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from hyprfire_app.exceptions import TimestampException
from hyprfire_app.utils import timestamp


class TimestampTest(TestCase):

    @patch('hyprfire_app.new_scripts.kalon.timestamp.validate_timestamp')
    def test_correct_timestamp_returns_correct_format(self, mock_validate_timestamp):
        """
        test_correct_timestamp

        convert_to_editcap_format should call validate_function once with the provided timestamp
        then return that value
        """
        ts = 100
        expected_output = datetime.fromtimestamp(ts)
        actual_output = timestamp.convert_to_editcap_format(ts)

        mock_validate_timestamp.assert_called_once_with(100)
        self.assertEqual(expected_output, actual_output)

    def test_incorrect_timestamp_raises_exception(self):
        """
        test_incorrect_timestamp

        An invalid timestamp should raise a TimestampException. If another exception is raised,
        something broke with the validate_timestamp call in convert_to_editcap_format
        """
        ts = 'hello'

        self.assertRaises(TimestampException, timestamp.convert_to_editcap_format, ts)

    def test_equal_timestamps_true(self):
        """
        test_timestamps_equal

        Two timestamps should be considered equal if they are the same to 9 decimal places
        """
        # Different at 10th dp
        first_ts = 2.0000000001
        second_ts = 2.0000000003

        self.assertTrue(timestamp.timestamps_equal(first_ts, second_ts))

    def test_unequal_timestamps_false(self):
        """
        test_timestamps_not_equal

        Two timestamps should not be considered equal if they are different to the 9th decimal place
        """
        # Different at 9th dp
        first_ts = 2.000000001
        second_ts = 2.000000003

        self.assertFalse(timestamp.timestamps_equal(first_ts, second_ts))
