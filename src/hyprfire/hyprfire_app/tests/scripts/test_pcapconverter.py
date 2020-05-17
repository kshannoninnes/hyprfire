import unittest
from src.hyprfire.hyprfire_app.new_scripts.converterexception import ConverterException
from src.hyprfire.hyprfire_app.new_scripts.pcapconverter import pcapConverter
from src.hyprfire.hyprfire.settings import BASE_DIR
from pathlib import Path
import time

class MyTestCase(unittest.TestCase):
    def test_pcapconverter(self):
        testpath = str(Path(BASE_DIR)/'hyprfire_app'/'tests'/'test_files'/'testdump')
        starttime = time.time()
        result = pcapConverter(testpath)
        runtime = time.time() - starttime
        expectedPackets = 11850
        self.assertEqual(1588259849.166453227, float(result[0].epochTimestamp), "First segment")
        self.assertEqual(1588259885.838919690, float(result[10000].epochTimestamp), "2nd")
        self.assertEqual(1588259889.284641293, float(result[-1].epochTimestamp), "last")
        self.assertEqual(expectedPackets, len(result), "Number of packets after filtering")

    #test using a non-existant filename
    def test_pcapconverter_nofile(self):
        with self.assertRaises(ConverterException) as cm:
            pcapConverter("fake.pcap")
        e = cm.exception
        self.assertEqual(e.message, "Filename does not exist")

    #test using a file that isn't a pcap file
    def test_pcapconverter_wrongfile(self):
        testpath = str(Path(BASE_DIR)/'hyprfire_app'/'new_scripts'/'pcapconverter.py')
        with self.assertRaises(ConverterException) as cm:
            pcapConverter(testpath)
        e = cm.exception
        self.assertEqual(e.message, "Editcap failure: is this file a capture file?")
