from django.test import TestCase
from hyprfire_app.new_scripts import reverse_mapping

from decimal import Decimal
from random import randint
from scapy.all import PcapReader
from hyprfire_app.utils.testing import remove_test_files, TEST_FILE


# Create your tests here.


def timestamps_equal(first, second):
    eps = 0.000001
    return abs(first - second) < eps


class ExportPacketsTestCase(TestCase):
    scapy_list = PcapReader(TEST_FILE).read_all()

    """
    setUp & tearDown

    Ensure that any non-relevant test files are removed from the test directories before and after running tests
    """
    def setUp(self):
        remove_test_files()

    def tearDown(self):
        remove_test_files()

    def test_correct_number_packets_collected(self):
        """
        test_correct_number_packets_collected

        The number of packets in the output_file should match the length of the test_packets list
        """
        expected_count = 20

        starting_packet = randint(0, len(self.scapy_list) - 1 - expected_count)
        test_packets = self.scapy_list[starting_packet:starting_packet + expected_count]

        output_file = reverse_mapping.export_packets_in_range(TEST_FILE,
                                                              test_packets[0].time,
                                                              test_packets[expected_count - 1].time)

        actual_count = len(PcapReader(output_file).read_all())

        self.assertEqual(actual_count, expected_count)

    def test_correct_packets_collected(self):
        """
        test_correct_packets_collected

        The timestamps for packets written to the output_file should match the timestamps for
        the packets in the test_packets list
        """
        packet_list = []
        num_packets = 5

        starting_packet = randint(0, len(self.scapy_list) - 1 - num_packets)
        test_packets = self.scapy_list[starting_packet:starting_packet+5]

        output_file = reverse_mapping.export_packets_in_range(TEST_FILE, test_packets[0].time, test_packets[4].time)
        for packet in PcapReader(output_file):
            packet_list.append(packet)

        for index, actual_packet in enumerate(packet_list):
            self.assertTrue(timestamps_equal(actual_packet.time, test_packets[index].time))

    def test_invalid_file(self):
        """
        test_invalid_file

        Invalid file should raise an IOError
        """
        filename = 'undefined'
        start_timestamp = Decimal(1588259870.211190166)
        end_timestamp = Decimal(1588259871.211190166)

        self.assertRaises(IOError, reverse_mapping.export_packets_in_range, filename, start_timestamp, end_timestamp)

    def test_negative_timestamp(self):
        """
        test_negative_timestamp

        Negative timestamp should raise a ValueError
        """
        start_timestamp = Decimal("-1")
        end_timestamp = Decimal("inf")

        self.assertRaises(ValueError, reverse_mapping.export_packets_in_range, TEST_FILE, start_timestamp, end_timestamp)

    def test_infinite_timestamp(self):
        """
        test_infinite_timestamp

        Infinite timestamp should raise a ValueError
        """
        start_timestamp = Decimal("inf")
        end_timestamp = Decimal("inf") + 1

        self.assertRaises(ValueError, reverse_mapping.export_packets_in_range, TEST_FILE, start_timestamp, end_timestamp)
