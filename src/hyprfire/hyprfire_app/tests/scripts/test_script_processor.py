'''
This is a testing file for the Module: CacheHandler's ScriptProcessor
A series of tests will run to check how the function will run.
Multiple functions will try different scenarios, causing the Script Processor to both fail and pass
'''

from django.test import TestCase
from hyprfire_app import CacheHandler as ch
import os
from hyprfire_app.models import Data

filename = os.path.abspath('hyprfire_app/tests/test_files/testdump')


class CacheHandlerTestCase(TestCase):

    def test_valid_arguments_none_cache(self):
        """
        This test function will run and test a none cached data
        It will check if the a string will be returned at the end with no error.

        The test file will be: testdump

        :return: True if a plotly, html graph has been created.
        """

        valid1 = ch.CacheHandler(filename, 'Benford', '1000', 'Time')
        valid2 = ch.CacheHandler(filename, 'Zipf', '2000', 'Length')

        self.assertIsInstance(valid1, str)
        self.assertIsInstance(valid2, str)

    def test_valid_arguments_cached(self):
        """
        This test function will run and test cached data. It will not go through Script Processor but instead
        go through the cached data.

        It will create a model, thats going to duplicate the inside of the data

        :return: True if a string is returned.
        """

        data = Data.objects.create(filename=filename, algorithm='Zipf', window_size=1000, analysis='Time', data="{}")
        data.save()

        valid1 = ch.CacheHandler(filename, 'Zipf', '1000', 'Time')

        self.assertIsInstance(valid1, str)


    def test_invalid_filename(self):
        """
        This test function will test how the ScriptProcessor will handle invalid filename names.
        Currently the ScriptProcessor will return a ValueError

        If a value error is not returned then the test has failed

        The test file will be: fake_testdump

        :return: True if test passes
        """
        fake_filename = os.path.abspath('hyprfire_app/tests/test_files/fake_testdump')

        with self.assertRaises(FileNotFoundError):
            ch.CacheHandler(fake_filename, 'Benford', '1000', 'Time')

    def test_invalid_windowsize(self):
        """
        This test function will test how the Script Processor will handle invalid windowsize input
        Currently the Script Processor will check if its valid or not and return a ValueError if its invalid

        The test file will be: testdump
        The Test passes if a Value Error is caught

        :return: True if test passes, False otherwise
        """

        with self.assertRaises(ValueError):
            ch.CacheHandler(filename, 'Zipf', '-1', 'Length')

    def test_invalid_algortihm(self):
        """
        This test function will test how the Script Processor will handle invalid algorithm input
        Currently the Script Processor will check for Benford and Zipf and return a ValueError if it is none of those

        The test file will be: testdump
        Test will pass if a ValueError is caught.

        :return: True if Test Passes and False otherwise
        """

        with self.assertRaises(ValueError):
            ch.CacheHandler(filename, 'Invalid', '2000', 'Time')

    def test_invalid_analysis(self):
        """
        This function will test if a ValueError will be thrown if the analysis type inputted is invalid
        analysis consists of only two option, 'Time' or 'Length' and should not accept anything else

        :return: True if a ValueError exception is thrown
        """
        with self.assertRaises(ValueError):
            ch.CacheHandler(filename, 'Benford', '1000', 'Invalid')