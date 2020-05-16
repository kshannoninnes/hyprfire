from django.test import TestCase

from hyprfire.settings import BASE_DIR
from hyprfire_app.exceptions import TimestampException
from hyprfire_app.new_scripts.kalon import validation, timestamp


class FileValidationTest(TestCase):
    def test_valid_file_pass(self):
        """
        test_valid_file_pass

        A valid file should not raise any exceptions
        """
        file = f'{BASE_DIR}/hyprfire_app/tests/test_files/testdump'

        self.assertEqual(file, validation.validate_file_path(file))

    def test_directory_fail(self):
        """
        test_directory_fail

        A directory should fail validation with a FileNotFoundError
        """
        file = f'{BASE_DIR}'

        self.assertRaises(FileNotFoundError, validation.validate_file_path, file)

    def test_invalid_file_fail(self):
        """
        test_invalid_file_fail

        An invalid file should fail validation with a FileNotFoundError
        """
        file = 'BADFILE'

        self.assertRaises(FileNotFoundError, validation.validate_file_path, file)


class TimestampValidationTest(TestCase):
    def test_zero_timestamp(self):
        """
        test_zero_timestamp

        A zero timestamp shouldn't throw any exceptions
        """
        ts = 0

        self.assertEqual(ts, validation.validate_timestamp(0))

    def test_invalid_timestamp_format(self):
        """
        test_invalid_timestamp_format

        A timestamp with an incorrect format (eg. a string) should fail with a TimestampException
        """
        self.assertRaises(TimestampException, validation.validate_timestamp, 'hello')

    def test_too_large_timestamp(self):
        """
        test_too_large_timestamp

        A timestamp that that is larger than 64 bit integer maximum should fail with a TimestampException
        """
        # This integer is the epoch timestamp for 3000-01-01 00:00:00
        max_int = 32503680000

        self.assertRaises(TimestampException, timestamp.validate_timestamp, max_int)

    def test_infinite_timestamp(self):
        """
        test_infinite_timestamp

        An infinite timestamp should fail with a TimestampException
        """
        self.assertRaises(TimestampException, validation.validate_timestamp, float("inf"))

    def test_negative_start(self):
        """
        test_negative_start

        A negative start time should fail with a TimestampException
        """
        self.assertRaises(TimestampException, validation.validate_timestamp, -1)
