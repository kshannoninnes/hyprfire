"""
File: test_packetdata_converter.py
Author: Quang Le
Purpose: unit tests for packetdata_converter.py
"""
from pathlib import Path
from hyprfire.settings import BASE_DIR
from hyprfire_app.new_scripts.pcapconverter import pcapConverter
from hyprfire_app.new_scripts import packetdata_converter
import unittest


class TestUnit(unittest.TestCase):

    def setUp(self):
        pcapfile = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        self.pcapdata = pcapConverter(pcapfile)

    def test_invalid_analysis_value(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'None', 1000, 't')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, self.pcapdata, 0, 1000, 't')

    def test_invalid_timelen_value(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 1000, 'None')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 1000, 0)

    def test_invalid_packetdata(self):
        invalid = "Invalid"
        empty = []
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, empty, 'b', 1000, 't')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, invalid, 'b', 1000, 't')

    def test_invalid_winsize(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 0, 't')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 'None', 't')

    def test_convert_benfords_time(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'b', 1000, 't')
        expected_len = 11
        self.assertTrue(isinstance(output, list))
        self.assertEqual(len(output), expected_len)

    def test_convert_benfords_length(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'b', 1000, 'l')
        expected_len = 11
        self.assertTrue(isinstance(output, list))
        self.assertEqual(len(output), expected_len)

    def test_convert_zipf_time(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'z', 1000, 't')
        expected_len = 11
        self.assertTrue(isinstance(output, list))
        self.assertEqual(len(output), expected_len)

    def test_convert_zipf_length(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'z', 1000, 'l')
        expected_len = 11
        self.assertTrue(isinstance(output, list))
        self.assertEqual(len(output), expected_len)
