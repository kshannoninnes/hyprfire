from pathlib import Path

from django.test import TestCase
from scapy.all import PcapReader

from hyprfire.settings import BASE_DIR
from hyprfire_app.filtering.packet_details_collector import PacketDetailsCollector


class TestPacketDetailsCollector(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        setUpClass

        Collecting packets and their details only needs to happen once per test suite
        """
        super(TestPacketDetailsCollector, cls).setUpClass()
        cls.packets = []

        num_packets = 20
        file = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        with PcapReader(file) as reader:
            while num_packets > 0:
                cls.packets.append(reader.read_packet())
                num_packets -= 1

        cls.packet_details = PacketDetailsCollector(cls.packets).get_details()

    def test_all_packets_match(self):
        """
        test_all_packets_match

        The filtered list should contain all packets in the original list
        """
        [self.assertEqual(str(x.time), str(self.packet_details[index]['timestamp']))
         for index, x in enumerate(self.packets)]

    def test_output_list_length_matches_original(self):
        """
        test_output_list_length_matches_original

        The size of the output list should match that of the original list
        """
        original_length = len(self.packets)
        output_length = len(self.packet_details)

        self.assertEqual(original_length, output_length)

