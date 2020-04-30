from django.test import TestCase
from hyprfire_app.new_scripts import reverse_mapping

from decimal import Decimal
from scapy.all import PcapReader
from pathlib import Path

# Create your tests here.


def remove_test_files():
    """
    remove_test_files

    Removes all test files created during testing
    """
    proj_root = Path(__file__).parent.parent
    test_dir = proj_root / 'pcaps' / 'exported_pcaps'

    for path in test_dir.glob('*'):
        if path.is_file():
            path.unlink()


class ExportPacketsTestCase(TestCase):

    def setUp(self):
        """
        setUp

        Ensure any pre-test case work is done before moving on to a new test case
        """
        remove_test_files()

    def tearDown(self):
        """
        tearDown

        Ensure any post-test case work is done before moving on to a new test case
        """
        remove_test_files()

    def test_correct_number_packets_collected(self):
        """
        test_correct_number_packets_collected

        Ensure that the packet list contains the correct number of packets
        """
        filename = 'dump16'
        end_timestamp = '1583398044.833782000'
        start_timestamp = '1583398044.833377000'
        expected_num_packets = 16
        actual_num_packets = 0

        output_path = reverse_mapping.export_packets(filename, start_timestamp, end_timestamp)
        for _ in PcapReader(output_path):
            actual_num_packets += 1

        self.assertEqual(actual_num_packets, expected_num_packets)

    def test_correct_packets_collected(self):
        """
        test_correct_packets_collected

        Ensure that the packet list contains the correct packets
        """
        filename = 'testdump'
        packet_list = []
        first_timestamp = '1588155523.764835000'
        second_timestamp = '1588155523.764843000'
        third_timestamp = '1588155523.766769000'
        fourth_timestamp = '1588155523.771269000'
        last_timestamp = '1588155523.771711000'

        output_path = reverse_mapping.export_packets(filename, first_timestamp, last_timestamp)
        for packet in PcapReader(output_path):
            packet_list.append(packet)

        # Decimal.compare returns 0 if the two values being compared are considered equivalent
        self.assertEqual(packet_list[0].time.compare(Decimal(first_timestamp)), 0)
        self.assertEqual(packet_list[1].time.compare(Decimal(second_timestamp)), 0)
        self.assertEqual(packet_list[2].time.compare(Decimal(third_timestamp)), 0)
        self.assertEqual(packet_list[3].time.compare(Decimal(fourth_timestamp)), 0)
        self.assertEqual(packet_list[4].time.compare(Decimal(last_timestamp)), 0)

    def test_invalid_file(self):
        """
        test_invalid_file

        Ensure correct exception is thrown when an invalid file is supplied.
        """
        filename = 'undefined'
        start_timestamp = '1583398791.536443000'
        end_timestamp = '1583398792.536443000'

        self.assertRaises(IOError, reverse_mapping.export_packets, filename, start_timestamp, end_timestamp)

    def test_invalid_timestamp(self):
        """
        test_invalid_timestamp

        Ensure correct exception is thrown when an invalid timestamp is supplied
        """
        filename = 'testdump'
        start_timestamp = '-1'
        end_timestamp = 5

        self.assertRaises(ValueError, reverse_mapping.export_packets, filename, start_timestamp, end_timestamp)
