import unittest

from hyprfire_app.new_scripts import plot_csvdata
from hyprfire_app.new_scripts.packetdata_converter import CSVData


class MyTestCase(unittest.TestCase):

    def setUp(self):
        row1 = CSVData(4056700, 0.00401, 1422423.4, 1565756.5)
        row2 = CSVData(4232342, 0.00423, 1576457.6, 1664468.7)
        row3 = CSVData(4355466, 0.00829, 1674534.6, 1735324.7)
        row4 = CSVData(4676547, 0.00437, 1783643.9, 1845545.6)
        row5 = CSVData(4854545, 0.00459, 1845454.4, 1945454.8)
        self.csvdata = [row1, row2, row3, row4, row5]

    def test_plot_success(self):
        graph = plot_csvdata.get_plot(self.csvdata)
        self.assertIsInstance(graph, str)

    def test_plot_invalid_data(self):
        data = "Invalid"
        self.assertRaises(TypeError, plot_csvdata.get_plot, data)


