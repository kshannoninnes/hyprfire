import unittest
from hyprfire_app.new_scripts.converterexception import ConverterException
from hyprfire_app.new_scripts.pcapconverter import pcapConverter
from hyprfire_app.new_scripts.packetdata import PacketData
import time
import os

class MyTestCase(unittest.TestCase):
    #test using 10000 packet pcap
    def test_pcapconverter(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        testpath = os.path.join(dirpath, "../new_scripts/test.pcap")
        packetFirst = PacketData(epochTimestamp=1583450242.343441000, timestamp=26242343441, len=88)
        packetLast = PacketData(epochTimestamp=1583450244.227514000, timestamp=26244227514, len=134)
        UDPpacket = PacketData(epochTimestamp=1583450242.345706, timestamp=26242345706, len=1466)
        starttime = time.time()
        result = pcapConverter(testpath)
        runtime = time.time() - starttime
        expectedPackets = 9999
        print(f"Execution took {runtime} seconds for 10000 packets")
        self.assertEqual(packetFirst, result.packets[0], "First packet comparison")
        self.assertEqual(packetLast, result.packets[-1], "Last packet comparison")
        self.assertEqual(UDPpacket, result.packets[8], "UDP packet comparison")
        self.assertEqual(expectedPackets, len(result.packets), "Number of packets after filtering")

    #test using a non-existant filename
    def test_pcapconverter_nofile(self):
        with self.assertRaises(ConverterException) as cm:
            pcapConverter("fake.pcap")
        e = cm.exception
        self.assertEqual(e.message, "Filename does not exist")

    #test using a file that isn't a pcap file
    def test_pcapconverter_wrongfile(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        testpath = os.path.join(dirpath, "../new_scripts/../../new_scripts/packetdata.py")
        with self.assertRaises(ConverterException) as cm:
            pcapConverter(testpath)
        e = cm.exception
        self.assertEqual(e.message, "Filename is not a supported capture file")
