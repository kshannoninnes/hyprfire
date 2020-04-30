'''
This is a testing file for the Module: CacheHandler's ScriptProcessor
A series of tests will run to check how the function will run.
Multiple functions will try different scenarios, causing the Script Processor to both fail and pass
'''

from django.test import TestCase
from hyprfire_app import CacheHandler as ch
import os


class ScriptProcessorTestCase(TestCase):

    def test_valid_arguments(self):
        """
        This test function will run ScriptProcessor with everything valid.
        If there is a file inside the ../../temp/ directory named: "dump2941benfedecit.tcpd.n2d_benf_time.csv
        This test function will return True.

        The test file will be: dump2941benfedit

        :return: True if a csv file is then created.
        """

        filename = os.path.abspath('../hyprfire/pcaps/dump2941benfedit')

        result_file = os.path.abspath("../hyprfire/temp/dump2941benfedit.tcpd.n2d_benf_time.csv")

        ch.ScriptProcessor(filename, 'Benford', '1000')

        if os.path.exists(result_file):
            print("csv test file found")
            answer = True
        else:
            print("csv test file not found")
            answer = False

        return answer

    def test_invalid_filename(self):
        """
        This test function will test how the ScriptProcessor will handle invalid filename names.
        Currently the ScriptProcessor will return a ValueError

        If a value error is not returned then the test has failed

        The test file will be: dump2941benfedit-fail (does not exist)

        :return: True if test passes
        """

        filename = os.path.abspath('../hyprfire/pcaps/dump2941benfedit-fail')

        answer = False

        try:
            ch.ScriptProcessor(filename, 'Benford', '1000')

        except ValueError:
            print("Value Error Throw works!")
            answer = True

        return answer


    def test_invalid_windowsize(self):
        """
        This test function will test how the Script Processor will handle invalid windowsize input
        Currently the Script Processor will check if its valid or not and return a ValueError if its invalid

        The test file will be: dump2941benfedit
        The Test passes if a Value Error is caught

        :return: True if test passes, False otherwise
        """

        filename = os.path.abspath('../hyprfire/pcaps/dump2941benfedit')

        answer = False

        try:
            ch.ScriptProcessor(filename, 'Benford', '500')

        except ValueError:
            print("Value Error Throw works for invalid window size")
            answer = True

        return answer

    def test_invalid_algortihm(self):
        """
        This test function will test how the Script Processor will handle invalid algorithm input
        Currently the Script Processor will check for Benford and Zipf and return a ValueError if it is none of those

        The test file will be: dump2941benfedit
        Test will pass if a ValueError is caught.

        :return: True if Test Passes and False otherwise
        """
        filename = os.path.abspath('../hyprfire/pcaps/dump2941benfedit')

        answer = False

        try:
            ch.ScriptProcessor(filename, 'Invalid', '2000')

        except ValueError:
            print("Value Error Throw works for invalid algorithm input")
            answer = True

        return answer
