from hyprfire_app.scripts.pcapconverter import pcapConverter
from hyprfire_app.scripts.tcpdumpconverter import tcpdumpConverter
from hyprfire_app.scripts.n2dconverter import convert

def requestHandler(filename):
    pcapConverter(filename)
    tcpdumpConverter(filename)
    convert(filename)
