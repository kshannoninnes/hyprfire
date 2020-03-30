from hyprfire_app.scripts.pcapconverter import pcapConverter
from hyprfire_app.scripts.tcpdumpconverter import tcpdumpConverter
import sys

def requestHandler(filename):
    pcapConverter(filename)
    tcpdumpConverter(filename)

if __name__ == '__main__':
    requestHandler()