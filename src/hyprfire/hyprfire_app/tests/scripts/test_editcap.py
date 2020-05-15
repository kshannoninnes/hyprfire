from django.test import TestCase
from pathlib import Path

from hyprfire.settings import BASE_DIR
from hyprfire_app.exceptions import TimestampException, EditcapException
from hyprfire_app.new_scripts.packet_manipulator import editcap


class EditcapTest(TestCase):
    def setUp(self):
        self.input_file = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        self.start = 1588259850
        self.end = 1588259850

    def test_correct(self):
        """
        test_correct

        Editcap should output a list of packets where all packets are between the start and
        end seconds of the provided timestamps
        """
        output = editcap.create_packet_list(self.input_file, self.start, self.end)

        for packet in output:
            packet_second = int(packet.time)
            self.assertGreaterEqual(packet_second, self.start)
            self.assertLessEqual(packet_second, self.end)

    def test_nonexistent_file(self):
        """
        test_nonexistent_file

        A nonexistent file should raise a FileNotFoundError
        """
        self.assertRaises(FileNotFoundError, editcap.create_packet_list, 'nonexistentfile', self.start, self.end)

    def test_early_end_timestamp(self):
        """
        test_early_end_timestamp

        An end timestamp before the start timestamp should raise an EditcapException
        """
        self.assertRaises(EditcapException, editcap.create_packet_list, self.input_file, self.start, self.start - 1)
