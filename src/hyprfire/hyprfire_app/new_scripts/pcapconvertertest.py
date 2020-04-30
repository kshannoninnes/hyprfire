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
        testpath = os.path.join(dirpath, "test.pcap")
        packetFirst = PacketData(epochTimestamp=1583450242.343441000, timestamp=26242343441, IPFrom='52.98.9.130', IPTo='10.162.72.24', portFrom=443, portTo=20570, len=34, winLen=2044, flags='0,1,0,0,1,0,0')
        packetLast = PacketData(epochTimestamp=1583450244.227514000, timestamp=26244227514, IPFrom='10.163.72.8', IPTo='10.163.120.5', portFrom=445, portTo=56258, len=80, winLen=256, flags='0,1,0,0,1,0,0')
        UDPpacket = PacketData(epochTimestamp=1583450242.345706, timestamp=26242345706, IPFrom='10.162.78.1', IPTo='10.162.76.4', portFrom=2055, portTo=2055, len=1424, winLen='N/A', flags='0,0,0,0,0,0,1')
        starttime = time.time()
        result = pcapConverter(testpath)
        runtime = time.time() - starttime
        filteredtotal = 9172
        print(f"Execution took {runtime} seconds for 10000 packets")
        self.assertEqual(packetFirst, result.packets[0], "First packet comparison")
        self.assertEqual(packetLast, result.packets[-1], "Last packet comparison")
        self.assertEqual(UDPpacket, result.packets[8], "UDP packet comparison")
        self.assertEqual(filteredtotal, len(result.packets), "Number of packets after filtering")

    #test using a non-existant filename
    def test_pcapconverter_nofile(self):
        with self.assertRaises(ConverterException) as cm:
            pcapConverter("fake.pcap")
        e = cm.exception
        self.assertEqual(e.message, "Filename does not exist")

    #test using a file that isn't a pcap file
    def test_pcapconverter_wrongfile(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        testpath = os.path.join(dirpath, "packetdata.py")
        with self.assertRaises(ConverterException) as cm:
            pcapConverter(testpath)
        e = cm.exception
        self.assertEqual(e.message, "Filename is not a supported capture file")

if __name__ == '__main__':
    unittest.main()
