from django.test import TestCase
from pathlib import Path
from hyprfire_app.new_scripts.data_extractor import get_data


# TODO Modify this to use a list of paths
# TODO Move this to a utils module for all tests
def remove_test_files():
    """
    remove_test_files

    Removes all test files created during testing
    """
    proj_root = Path(__file__).parent.parent.parent
    test_dir = proj_root / 'pcaps' / 'exported_pcaps'

    for path in test_dir.glob('*'):
        if path.is_file():
            path.unlink()


class GetDataTestCase(TestCase):

    def setUp(self):
        """
        setUp

        Ensure any pre-test case work is done before moving on to a new test case
        """
        remove_test_files()

    def tearDown(self):
        """
        tearDown

        Ensure any post-test case work is done before moving on to a new test case
        """
        remove_test_files()

    def test_correct_protocol(self):
        pcap_data = get_data('testdump')
        input()
