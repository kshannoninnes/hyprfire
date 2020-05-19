import random
from pathlib import Path

from django.test import TestCase
from scapy.all import PcapReader

from hyprfire.settings import BASE_DIR
from hyprfire_app.filtering.packet_filter import PacketFilter


class TestPacketFilter(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPacketFilter, cls).setUpClass()

        num_packets = 20
        file = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        full_list = PcapReader(file).read_all()
        start_packet = random.choice(range(0, len(full_list) - 1 - num_packets))

        cls.original_list = full_list[start_packet:start_packet + num_packets]
        cls.actual_list = \
            PacketFilter(file, str(cls.original_list[0].time), str(cls.original_list[-1].time)).get_filtered_list()

    def test_filtered_list_contains_all_correct_packets(self):
        """
        test_filtered_list_contains_all_correct_packets

        The output filtered list should contain all packets with a timestamp between start and end, inclusive
        """
        [self.assertEqual(str(expected.time), str(self.actual_list[index].time))
         for index, expected in enumerate(self.original_list)]

    def test_output_list_length_matches_original(self):
        """
        test_list_lengths_match

        The output filtered list's length should match that of the original list
        """
        self.assertEqual(len(self.actual_list), len(self.original_list))

    def test_empty_file_outputs_empty_list(self):
        """
        test_empty_file_outputs_empty_list

        If an empty file is passed in, the output should be an empty list
        """
        empty_file = Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'empty'

        if not empty_file.exists():
            empty_file.touch()

        empty_list = PacketFilter(str(empty_file)).get_filtered_list()
        empty_file.unlink()

        self.assertEqual(len(empty_list), 0)
