from scapy.contrib.mount import Path


def get_filename_list(path):
    """
    get_filename_list

    Helper function to retrieve a list of non-hidden filenames from a directory

    Parameters
    path: a path to a directory containing files

    Return
    A list of non-hidden filenames in the directory
    """
    file_list = Path(path).glob('*')
    filenames = []

    for file in file_list:
        name = file.stem.lower()
        if file.is_file() and not name.startswith('.'):
            filenames.append(name)

    return filenames
