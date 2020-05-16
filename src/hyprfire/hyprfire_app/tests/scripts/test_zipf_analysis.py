"""
File: test_zipf_analysis.py
Author: Quang Le
Purpose: unit test for zipf_analysis.py
"""

import unittest
from hyprfire_app.new_scripts import zipf_analysis


class TestZipfUnit(unittest.TestCase):

    def test_buckets_success(self):
        num_list = [1000, 3000, 500, 800]
        expected = [0.25, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        actual = zipf_analysis.get_zipf_buckets(num_list)
        self.assertEqual(actual, expected)

    def test_u_value_success(self):
        prob_list = [0.25, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        actual = zipf_analysis.get_zipf_u_value(prob_list)
        expected = 0.01977626255580357
        self.assertEqual(actual, expected)

    def test_weight_invalid_index(self):
        invalid_idx = 12
        in_list = [0.25, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertRaises(IndexError, zipf_analysis.get_watson_weight, invalid_idx, in_list)

