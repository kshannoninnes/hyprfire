from pathlib import Path
import random

from django.test import TestCase
from scapy.all import PcapReader
from scapy.layers.inet import IP

from hyprfire.settings import BASE_DIR
from hyprfire_app.new_scripts.kalon.packet_details_collector import PacketDetailsCollector


class TestPacketDetailsCollector(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPacketDetailsCollector, cls).setUpClass()
        cls.packets = []

        num_packets = 20
        file = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        with PcapReader(file) as reader:
            while num_packets > 0:
                cls.packets.append(reader.read_packet())
                num_packets -= 1

        cls.packet_details = PacketDetailsCollector(cls.packets).get_details()

    def setUp(self):
        packet_num = random.choice(range(0, len(self.packets) - 1))
        self.expected_packet = self.packets[packet_num]
        self.actual_packet = self.packet_details[packet_num]

    def test_random_packets_match(self):
        """
        test_random_packets_match

        Any given packet in the original list should match the same packet in the output list

        Note: we compare several packet attributes together as a package to ensure uniqueness
        """
        self.assertEqual(str(self.expected_packet.time), self.actual_packet['timestamp'])
        self.assertEqual(str(self.expected_packet[IP].src), self.actual_packet['ip_data']['src'])
        self.assertEqual(str(self.expected_packet[IP].dst), self.actual_packet['ip_data']['dst'])

    def test_output_list_length_matches_original(self):
        """
        test_output_list_length_matches_original

        The size of the output list should match that of the original list
        """
        original_length = len(self.packets)
        output_length = len(self.packet_details)

        self.assertEqual(original_length, output_length)

