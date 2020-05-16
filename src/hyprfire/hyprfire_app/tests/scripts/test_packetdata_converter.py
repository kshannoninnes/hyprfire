"""
File: test_packetdata_converter.py
Author: Quang Le
Purpose: unit tests for packetdata_converter.py
"""

from hyprfire_app.new_scripts.pcapconverter import pcapConverter
from hyprfire_app.new_scripts import packetdata_converter
import unittest


class TestUnit(unittest.TestCase):

    def setUp(self):
        pcapfile = '../test_files/testfile.pcap.gz'
        self.pcapdata = pcapConverter(pcapfile)

    def test_invalid_analysis_value(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'a', 1000, 't')

    def test_invalid_timelen_value(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 1000, 0)

    def test_invalid_packetdata(self):
        data = "Invalid"
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, data, 'b', 1000, 't')

    def test_invalid_winsize(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 0, 't')

    def test_convert_success(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'b', 1000, 't')
        expected = False
        if isinstance(output, list):
            expected = True
        self.assertTrue(expected)
