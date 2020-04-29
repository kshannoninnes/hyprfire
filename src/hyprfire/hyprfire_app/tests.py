from django.test import TestCase
from hyprfire_app.new_scripts import reverse_mapping

from decimal import Decimal
from scapy.all import PcapReader
from pathlib import Path

# Create your tests here.


class ExportPacketsTestCase(TestCase):

    def tearDown(self):
        """
        tearDown

        Ensure any post-test case work is done before moving on to a new test case
        """
        # Remove exported file file
        proj_root = Path(__file__).parent.parent
        test_dir = proj_root / 'pcaps' / 'exported_pcaps'

        for path in test_dir.glob('*.pcap'):
            if path.is_file():
                path.unlink()

    def test_correct_number_packets_collected(self):
        """
        test_correct_number_packets_collected

        Ensure that the packet list contains the correct number of packets
        """
        filename = 'dump16'
        expected_num_packets = 5
        timestamp = '1583398791.537257000'
        actual_num_packets = 0

        output_path = reverse_mapping.export_packets(filename, timestamp, expected_num_packets)
        for _ in PcapReader(output_path):
            actual_num_packets += 1

        self.assertEqual(actual_num_packets, expected_num_packets)
        self.tearDown()

    def test_correct_packets_collected(self):
        """
        test_correct_packets_collected

        Ensure that the packet list contains the correct packets
        """
        filename = 'testdump'
        num_packets = 5
        packet_list = []
        first_timestamp = '1583398791.537257000'
        second_timestamp = '1583398791.537258000'
        third_timestamp = '1583398791.537259000'
        fourth_timestamp = '1583398791.537260000'
        fifth_timestamp = '1583398791.537309000'

        output_path = reverse_mapping.export_packets(filename, first_timestamp, num_packets)
        for packet in PcapReader(output_path):
            packet_list.append(packet)

        # Decimal.compare returns 0 if the two values being compared are considered equivalent
        self.assertEqual(packet_list[0].time.compare(Decimal(first_timestamp)), 0)
        self.assertEqual(packet_list[1].time.compare(Decimal(second_timestamp)), 0)
        self.assertEqual(packet_list[2].time.compare(Decimal(third_timestamp)), 0)
        self.assertEqual(packet_list[3].time.compare(Decimal(fourth_timestamp)), 0)
        self.assertEqual(packet_list[4].time.compare(Decimal(fifth_timestamp)), 0)
        self.tearDown()

    def test_invalid_file(self):
        """
        test_invalid_file

        Ensure correct exception is thrown when an invalid file is supplied.
        """
        filename = 'undefined'
        num_packets = 5
        timestamp = '1583398791.536443000'

        self.assertRaises(IOError, reverse_mapping.export_packets, filename, timestamp, num_packets)
        self.tearDown()

    def test_invalid_timestamp(self):
        """
        test_invalid_timestamp

        Ensure correct exception is thrown when an invalid timestamp is supplied
        """
        filename = 'testdump'
        num_packets = 5
        timestamp = '-1'

        self.assertRaises(ValueError, reverse_mapping.export_packets, filename, timestamp, num_packets)
        self.tearDown()
