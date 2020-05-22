"""
File: test_packetdata_converter.py
Author: Quang Le
Purpose: unit tests for packetdata_converter.py
"""
from pathlib import Path
from hyprfire.settings import BASE_DIR
from hyprfire_app.analysis.pcapconverter import pcapConverter
from hyprfire_app.analysis import packetdata_converter
import unittest


class PacketDataConverterTestUnit(unittest.TestCase):

    def setUp(self):
        pcapfile = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')
        self.pcapdata = pcapConverter(pcapfile)

    # Test invalid convert_to_csv parameters raises errors correctly===================================================
    def test_invalid_anatype_raises_errors(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'None', 1000, 't')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, self.pcapdata, 0, 1000, 't')

    def test_invalid_timelen_value_raises_errors(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 1000, 'None')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 1000, 0)

    def test_invalid_packetdata_raises_errors(self):
        invalid = "Invalid"
        empty = []
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, empty, 'b', 1000, 't')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, invalid, 'b', 1000, 't')

    def test_invalid_winsize_raises_errors(self):
        self.assertRaises(ValueError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 0, 't')
        self.assertRaises(TypeError, packetdata_converter.convert_to_csv, self.pcapdata, 'b', 'None', 't')

    # Test convert_to_csv is successful with all four possible config options==========================================
    def test_convert_benfords_time_success(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'b', 1000, 't')
        expected_len = 11
        print(output)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), expected_len)

    def test_convert_benfords_length_success(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'b', 1000, 'l')
        expected_len = 11
        print(output)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), expected_len)

    def test_convert_zipf_time_success(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'z', 1000, 't')
        expected_len = 11
        print(output)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), expected_len)

    def test_convert_zipf_length_success(self):
        output = packetdata_converter.convert_to_csv(self.pcapdata, 'z', 1000, 'l')
        expected_len = 11
        print(output)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), expected_len)
