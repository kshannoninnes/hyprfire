import string
from pathlib import Path
from random import random

from django.test import TestCase

from hyprfire.settings import BASE_DIR
from hyprfire_app.new_scripts.kalon.file import get_filename_list


class FileTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(FileTest, cls).setUpClass()
        cls.test_dir = Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files'

    def test_hidden_files_not_in_returned_list(self):
        """
        test_hidden_files_not_in_returned_list

        Hidden files should not be present in the output filename list
        """
        hidden_file_name = '.hidden'
        hidden_file = Path(self.test_dir / hidden_file_name)

        if not hidden_file.exists():
            hidden_file.touch()
        self.assertNotIn(hidden_file_name, get_filename_list(self.test_dir))
        hidden_file.unlink()

    def test_directories_not_in_returned_list(self):
        """
        test_directories_not_in_returned_list

        Directories should not be included in the output filename list
        """
        dir_name = 'test_dir'
        directory = Path(self.test_dir / dir_name)

        if not directory.exists():
            directory.mkdir()
        self.assertNotIn(dir_name, get_filename_list(self.test_dir))
        directory.rmdir()

    def test_returns_all_files_in_dir(self):
        """
        test_returns_all_files_in_dir

        get_filename_list should return all non-hidden file names from the specified directory
        """
        file_list = []
        quick_test_dir = Path(self.test_dir) / 'quick_test'
        if not quick_test_dir.exists():
            quick_test_dir.mkdir()

        for _ in range(0, 3):
            file_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
            new_file = quick_test_dir / file_name
            if not new_file.exists():
                new_file.touch()
            file_list.append(file_name)

        [self.assertIn(x, file_list) for x in get_filename_list(quick_test_dir)]

        for file in quick_test_dir.glob('*'):
            file.unlink()
        quick_test_dir.rmdir()
