from django.test import TestCase
from hyprfire_app.new_scripts import reverse_mapping

from decimal import Decimal
from scapy.all import PcapReader
from hyprfire_app.utils.testing import remove_test_files, TEST_FILE

# Create your tests here.


def timestamps_equal(first, second):
    eps = 0.000001
    return abs(first - second) < eps


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
        start_timestamp = '1588259869.856041149'
        end_timestamp = '1588259869.862443020'
        expected_num_packets = 20
        actual_num_packets = 0

        output_path = reverse_mapping.export_packets(TEST_FILE, start_timestamp, end_timestamp)
        for _ in PcapReader(output_path):
            actual_num_packets += 1

        self.assertEqual(actual_num_packets, expected_num_packets)

    def test_correct_packets_collected(self):
        """
        test_correct_packets_collected

        Ensure that the packet list contains the correct packets
        """
        packet_list = []
        first_timestamp = '1588259869.969993977'
        second_timestamp = '1588259869.970000623'
        third_timestamp = '1588259869.970755235'
        fourth_timestamp = '1588259869.970759984'
        last_timestamp = '1588259869.971553914'

        output_path = reverse_mapping.export_packets(TEST_FILE, first_timestamp, last_timestamp)
        for packet in PcapReader(output_path):
            packet_list.append(packet)

        # Decimal.compare returns 0 if the two values being compared are considered equivalent
        self.assertTrue(timestamps_equal(Decimal(first_timestamp), packet_list[0].time))
        self.assertTrue(timestamps_equal(Decimal(second_timestamp), packet_list[1].time))
        self.assertTrue(timestamps_equal(Decimal(third_timestamp), packet_list[2].time))
        self.assertTrue(timestamps_equal(Decimal(fourth_timestamp), packet_list[3].time))
        self.assertTrue(timestamps_equal(Decimal(last_timestamp), packet_list[4].time))

    def test_invalid_file(self):
        """
        test_invalid_file

        Ensure correct exception is thrown when an invalid file is supplied.
        """
        filename = 'undefined'
        start_timestamp = '1588259870.211190166'
        end_timestamp = '1588259871.211190166'

        self.assertRaises(IOError, reverse_mapping.export_packets, filename, start_timestamp, end_timestamp)

    def test_invalid_timestamp(self):
        """
        test_invalid_timestamp

        Ensure correct exception is thrown when an invalid timestamp is supplied
        """
        start_timestamp = '-1'
        end_timestamp = 'infinity'

        self.assertRaises(ValueError, reverse_mapping.export_packets, TEST_FILE, start_timestamp, end_timestamp)
