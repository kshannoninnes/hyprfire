from unittest import TestCase
from hyprfire_app.exceptions import ConverterException
from hyprfire_app.analysis import pcapconverter
from hyprfire.settings import BASE_DIR
from pathlib import Path
from decimal import Decimal
import random

class TestPcapConverter(TestCase):
    """ test pcapConverter in normal conditions; checks timestamps of the first packet, the first packet
    of the second file created by editcap, and the last packet against their equivalents in Wireshark
    also checks the number of packets against Wireshark, and whether the temporary files created during
    the process have successfully been deleted """
    def test_pcapconverter(self):
        testpath = str(Path(BASE_DIR)/'hyprfire_app'/'tests'/'test_files'/'testdump')
        result = pcapconverter.pcapConverter(testpath)
        exists = False
        check_deleted = Path(str(Path(BASE_DIR)/'hyprfire_app')).glob('temp*.pcap')
        for x in check_deleted:
            if x.is_file():
                exists = True

        self.assertEqual(1588259849.166453227, float(result[0].epochTimestamp))
        self.assertEqual(1588259885.838919690, float(result[10000].epochTimestamp))
        self.assertEqual(1588259889.284641293, float(result[-1].epochTimestamp))
        self.assertEqual(11850, len(result))
        self.assertFalse(exists)

    #test pcapConverter using a non-existant filename; should throw an exception
    def test_pcapconverter_nofile(self):
        rand = str(random.getrandbits(128)) + '.pcap'
        testpath = str(Path(BASE_DIR) / 'hyprfire_app' / 'new_scripts' / rand)
        with self.assertRaises(ConverterException) as cm:
            pcapconverter.pcapConverter(testpath)
        e = cm.exception

        self.assertEqual(e.message, "Filename does not exist")

    #test pcapConverter using a file that isn't a pcap file; should throw an exception
    def test_pcapconverter_wrongfile(self):
        testpath = str(Path(BASE_DIR)/'hyprfire_app'/'analysis'/'pcapconverter.py')
        with self.assertRaises(ConverterException) as cm:
            pcapconverter.pcapConverter(testpath)
        e = cm.exception

        self.assertEqual(e.message, "Editcap failure: is this file a capture file?")

    """ test extractData under normal conditions; checks timestamps of first and last packets against
    their equivalents in Wireshark, along with the total number of packets
    Note that pcapConverter should throw exceptions for incorrect filenames or filetypes before
    reaching extractData """
    def test_extractData(self):
        testpath = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        result = pcapconverter.extractData(testpath)

        self.assertEqual(1588259849.166453227, float(result[0].epochTimestamp), "First segment")
        self.assertEqual(1588259889.284641293, float(result[-1].epochTimestamp), "last")
        self.assertEqual(11850, len(result))

    """ test sinceMidnight
    Note that Decimal creates some strange rounding issues, so the number passed into sinceMidnight is
    actually 1588259850.7007715702056884765625, so result is tested accordingly """
    def test_sinceMidnight(self):
        val = Decimal('1588259850.700771485')
        result = pcapconverter.sinceMidnight(val)

        self.assertEqual(Decimal('83850700771.485'), result)