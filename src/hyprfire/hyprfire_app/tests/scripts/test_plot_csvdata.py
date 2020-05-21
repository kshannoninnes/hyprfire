"""
File: test_packetdata_converter.py
Author: Quang Le
Purpose: unit tests for plot_csvdata.py
"""

import unittest
from hyprfire_app.analysis import plot_csvdata


class PlotCSVDataTestUnit(unittest.TestCase):

    def setUp(self):
        row1 = "4056700,0.00401,1422423.4,1565756.5"
        row2 = "4232342,0.00423,1576457.6,1664468.7"
        row3 = "4355466,0.00829,1674534.6,1735324.7"
        row4 = "4676547,0.00437,1783643.9,1845545.6"
        row5 = "4854545,0.00459,1845454.4,1945454.8"
        invalid = "4854545,0.00459,1845454.4"
        self.csvdata = [row1, row2, row3, row4, row5]
        self.invalid_csv = [row1, row2, invalid, row3]

    #Test get_plot returns a string as expected
    def test_get_plot_success(self):
        graph = plot_csvdata.get_plot(self.csvdata)
        self.assertIsInstance(graph, str)

    #Test get_plot with invalid data raises errors as expected
    def test_plot_invalid_csvdata_raise_errors(self):
        data = "Invalid"
        empty = []
        self.assertRaises(ValueError, plot_csvdata.get_plot, empty)
        self.assertRaises(TypeError, plot_csvdata.get_plot, data)

    #Test customdata appears in the HTML string as expected
    def test_customdata_in_html(self):
        graph = plot_csvdata.get_plot(self.csvdata)
        expected = '"customdata": [["1422423.4", "1565756.5"], ["1576457.6", "1664468.7"], ["1674534.6", "1735324.7"],' \
                   ' ["1783643.9", "1845545.6"], ["1845454.4", "1945454.8"]'
        self.assertIn(expected, graph)

    #Test get_csv_values raises error correctly when iterating an invalid csv
    def test_get_csv_values_raise_error(self):
        self.assertRaises(IndexError, plot_csvdata.get_csv_values, self.invalid_csv)


