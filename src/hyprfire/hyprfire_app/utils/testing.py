from pathlib import Path
from hyprfire.settings import BASE_DIR
from .misc import EXPORTED_PCAP_DIR

TEST_FILE = str(Path(BASE_DIR) / 'hyprfire_app' / 'tests' / 'test_files' / 'testdump')


def remove_test_files():
    """
    remove_test_files

    Removes all test files created during testing
    """
    for path in EXPORTED_PCAP_DIR.glob('*'):
        if path.is_file():
            path.unlink()
