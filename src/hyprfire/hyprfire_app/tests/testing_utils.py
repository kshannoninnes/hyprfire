from pathlib import Path

TEST_FILE = str(Path(__file__).parent.parent.parent / 'pcaps' / 'testdump')


def remove_test_files():
    """
    remove_test_files

    Removes all test files created during testing
    """
    proj_root = Path(__file__).parent.parent.parent
    output_dir = proj_root / 'pcaps' / 'exported_pcaps'

    for path in output_dir.glob('*'):
        if path.is_file():
            path.unlink()
