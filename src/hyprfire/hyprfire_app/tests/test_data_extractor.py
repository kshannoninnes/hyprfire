from django.test import TestCase
from hyprfire_app.new_scripts.packet_manipulator.data_extractor import get_packet_data
from scapy.all import PcapReader
from random import randint
from hyprfire_app.utils.testing import remove_test_files, TEST_FILE


class GetDataTestCase(TestCase):
    scapy_list = PcapReader(TEST_FILE).read_all()

    """
    setUp & tearDown

    Ensure that any non-relevant test files are removed from the test directories before and after running tests
    """
    def setUp(self):
        remove_test_files()

    def tearDown(self):
        remove_test_files()

    def test_correctly_sized_list(self):
        """
        test_correctly_sized_list

        Ensure the list returned from get_packet_data has the same number of packets as the original pcap file
        """
        pcap_data = get_packet_data(TEST_FILE)

        self.assertEqual(len(pcap_data), len(self.scapy_list))

    def test_compare_random_packet(self):
        """
        test_compare_random_packet

        Compare a random packet from the original file with the same packet in the returned list to ensure
        both are the same
        """
        module_list = get_packet_data(TEST_FILE)
        packet_num = randint(0, len(module_list) - 1)

        scapy_packet_ts = str(self.scapy_list[packet_num].time)
        module_packet_ts = module_list[packet_num]['timestamp']

        self.assertEqual(scapy_packet_ts, module_packet_ts)
