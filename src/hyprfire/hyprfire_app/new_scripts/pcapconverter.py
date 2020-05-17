# pcapconverter.py: converts packets from a pcap file into a list of PacketData objects
# representing that file.
# pcapConverter takes a filename (with extension) and uses the PcapReader method from the Scapy library to
# extract information about each packet from the pcap file. ExtractData does the actual work.
# Will raise a ConverterException if the filename doesn't exist or isn't a pcap file.
# Author: Dean Quaife
# Last edited: 2020/05/15

from scapy.all import PcapReader
from src.hyprfire.hyprfire_app.new_scripts.packetdata import PacketData
from src.hyprfire.hyprfire_app.new_scripts.converterexception import ConverterException
import datetime, subprocess, multiprocessing
from pathlib import Path
from decimal import Decimal

#main pcapconverter method; takes in a pcap filename, splits it using editcap and returns a PacketData list
def pcapConverter(filename):
    if not Path(filename).is_file():
        raise ConverterException("Filename does not exist")

    cores = multiprocessing.cpu_count()
    temppaths = []
    dataList = []
    temp = "temp.pcap"
    command = f'editcap -c 10000 {filename} {temp}'
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise ConverterException(f"Editcap failure: is this file a capture file?")
    for x in Path('.').glob('temp*.pcap'):
        temppaths.append(str(x))
    with multiprocessing.Pool(processes=cores)as pool:
        res = pool.map(extractData, temppaths)
    for list in sorted(res, key= lambda list: list[0].epochTimestamp):
        dataList += list
    for x in Path('.').glob('temp*.pcap'):
        Path(x).unlink()
    return dataList

#converts important data from each editcap file into a list of PacketData objects
def extractData(file):
    packets = []
    for packet in PcapReader(file):
        epochTimestamp = Decimal(str(packet.time))
        timestamp = sinceMidnight(epochTimestamp)  # used to match timestamp to Stefan's original script
        len = packet.wirelen
        packets.append(PacketData(epochTimestamp, timestamp, len))
    return packets

#returns number of microseconds since midnight on the day the packet arrived; matches Stefan's original script
def sinceMidnight(epochTimestamp):
    date = datetime.datetime.fromtimestamp(epochTimestamp)
    hours = date.hour
    minutes = date.minute + 60 * hours
    seconds = date.second + 60 * minutes
    microseconds = date.microsecond + 1000000 * seconds
    return microseconds