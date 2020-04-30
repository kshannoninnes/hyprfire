"""
File: test_n2dconverter.py
Author: Quang Le
Purpose: unit tests for n2dconverter.py
"""


from hyprfire_app.new_scripts.pcapconverter import pcapConverter
from hyprfire_app.new_scripts import n2dconverter
import unittest


class TestUnit(unittest.TestCase):

    def setUp(self):
        self.pcapfile = "54"
        self.pcapdata = pcapConverter(self.pcapfile)

    def test_invalid_analysis_value(self):
        self.assertRaises(ValueError, n2dconverter.convert_to_csv, self.pcapdata, 'a', 1000, 't')

    def test_invalid_timelen_value(self):
        self.assertRaises(ValueError, n2dconverter.convert_to_csv, self.pcapdata, 'b', 1000, 0)

    def test_invalid_dumpfile(self):
        data = "Invalid"
        self.assertRaises(TypeError, n2dconverter.convert_to_csv, data, 'b', 1000, 't')

    def test_invalid_winsize(self):
        self.assertRaises(ValueError, n2dconverter.convert_to_csv, self.pcapdata, 'b', 0, 't')

    def test_convert_success(self):
        output = n2dconverter.convert_to_csv(self.pcapdata, 'b', 1000, 't')
        expected = False
        if isinstance(output, list):
            expected = True
        self.assertTrue(expected)





