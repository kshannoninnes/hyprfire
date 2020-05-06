from pathlib import Path
from hyprfire.settings import BASE_DIR


PCAP_DIR = Path(BASE_DIR) / 'pcaps'
EXPORTED_PCAP_DIR = PCAP_DIR / 'exported_pcaps'


def floats_equal(first, second):
    eps = 0.000001
    return abs(first - second) < eps
