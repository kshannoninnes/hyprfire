from django.test import TestCase
from hyprfire_app.new_scripts.data_extractor import get_packet_data
from scapy.all import PcapReader
from random import randint
from .testing_utils import remove_test_files, TEST_FILE


class GetDataTestCase(TestCase):

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

    def test_correctly_sized_list(self):
        """
        test_correctly_sized_list

        Ensure the list returned from get_packet_data has the same number of packets as the original pcap file
        """

        with PcapReader(TEST_FILE) as reader:
            pcap_data = get_packet_data(TEST_FILE)
            test_file_num_packets = len(reader.read_all())

            self.assertEqual(len(pcap_data), test_file_num_packets)

    def test_compare_random_packet(self):
        """
        test_compare_random_packet

        Compare a random packet from the original file with the same packet in the returned list to ensure
        both are the same
        """
        module_list = get_packet_data(TEST_FILE)
        packet_num = randint(0, len(module_list) - 1)

        with PcapReader(TEST_FILE) as reader:
            scapy_list = reader.read_all()
            scapy_packet_ts = str(scapy_list[packet_num].time)
            module_packet_ts = module_list[packet_num]['timestamp']

            self.assertEqual(scapy_packet_ts, module_packet_ts)
