from pathlib import Path

from django.test import TestCase
from scapy.all import PcapReader, PcapWriter

from hyprfire.settings import BASE_DIR
from hyprfire_app.utils.pcap import write_packets_to_file, read_packets_from_file


class PcapTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(PcapTest, cls).setUpClass()
        cls.packets = []
        cls.test_file = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'test_file')

        num_packets = 20
        file = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        with PcapReader(file) as reader:
            while num_packets > 0:
                cls.packets.append(reader.read_packet())
                num_packets -= 1

    def tearDown(self):
        file = Path(self.test_file)
        if file.exists() and file.is_file():
            file.unlink()

    def test_packets_are_written_to_file(self):
        """
        test_packets_are_written_to_file

        The packets written to file should match self.packets
        """
        write_packets_to_file(self.test_file, self.packets)
        result_list = PcapReader(self.test_file).read_all()

        # For each packet in self.packets, assert it exists in result_list
        [self.assertIn(x, result_list) for x in self.packets]

    def test_packets_in_file_match_packet_list(self):
        """
        test_packets_in_file_match_packet_list

        The packets in the list returned from read_packets_from_file should match self.packets
        """
        with PcapWriter(self.test_file, append=False) as writer:
            for packet in self.packets:
                writer.write(packet)

        result_list = read_packets_from_file(self.test_file)

        # For each packet in self.packets, assert it exists in result_list
        [self.assertIn(x, result_list) for x in self.packets]
