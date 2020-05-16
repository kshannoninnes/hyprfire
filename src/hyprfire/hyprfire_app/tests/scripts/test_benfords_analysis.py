"""
File: test_benfords_analysis.py
Author: Quang Le
Purpose: unit test for benfords_analysis.py
"""

from hyprfire_app.new_scripts import benfords_analysis
import unittest


class TestBenfordsUnit(unittest.TestCase):

    def test_interarrival_success(self):
        time_list = [10000, 12000, 14500, 16000]
        expected = [0, 2000, 2500, 1500]
        actual = benfords_analysis.get_interarrival_times(time_list)
        self.assertEqual(actual, expected)

    def test_interarrival_fail(self):
        time_list = [10000, 8000, 6000, 2000]
        self.assertRaises(ValueError, benfords_analysis.get_interarrival_times, time_list)

    def test_buckets_success(self):
        num_list = [0, 4000, 3000, 5000, 1000]
        index = 1
        expected  = [0.0, 0.25, 0.0, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0, 0.0]
        actual = benfords_analysis.get_benfords_buckets(num_list, index)
        self.assertEqual(actual, expected)

    def test_buckets_invalid_index(self):
        num_list = [0, 4000, 3000, 5000, 1000]
        index = 0
        self.assertRaises(ValueError, benfords_analysis.get_benfords_buckets, num_list, index)

    def test_u_value_success(self):
        prob_list = [0.0, 0.25, 0.0, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0, 0.0]
        idx = 1
        expected = 0.09491174999999998
        actual = benfords_analysis.get_benfords_u_value(prob_list, idx)
        self.assertEqual(actual, expected)

    def test_u_value_fail(self):
        idx = 0
        prob_list = [0.0, 0.25, 0.0, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0, 0.0]
        self.assertRaises(ValueError, benfords_analysis.get_benfords_u_value, prob_list, idx)

