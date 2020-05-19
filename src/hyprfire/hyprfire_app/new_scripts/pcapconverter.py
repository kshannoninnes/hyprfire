"""
pcapconverter.py: converts packets from a pcap file into a list of PacketData objects
representing that file.
pcapConverter takes a filename (with extension) and calls editcapSplit, which uses editcap
(a command provided by Wireshark) to split the file into smaller files of 10000 packets each.
It then uses a pool of processes to run the extractData method on each of them concurrently.
extractData calls the Scapy library method PcapReader to obtain information about each packet and
convert it into a list of PacketData objects to be provided to packetdataConverter. The data from
each smaller file is compiled together and sorted, then returned.
Author: Dean Quaife
Last edited: 2020/05/19
"""

from scapy.all import PcapReader
from hyprfire_app.new_scripts.packetdata import PacketData
from hyprfire_app.exceptions import ConverterException
import datetime, subprocess, multiprocessing
from pathlib import Path
from decimal import Decimal

""" retrieves data from a pcap file. Returns a PacketData list
will raise a ConverterException if filename doesn't exist or isn't a pcap file """
def pcapConverter(filename):
    cores = multiprocessing.cpu_count()
    temp_paths = []
    data_list = []

    if not Path(filename).is_file():
        raise ConverterException("Filename does not exist")
    try:
        editcapSplit(filename)
    except subprocess.CalledProcessError:
        raise ConverterException(f"Editcap failure: is this file a capture file?")

    for x in Path('.').glob('temp*.pcap'):
        temp_paths.append(str(x))
    with multiprocessing.Pool(processes=cores)as pool:
        res = pool.map(extractData, temp_paths) #pass temp filenames to extractData with multiprocessing

    for segment in sorted(res, key= lambda temp_data: temp_data[0].epochTimestamp):
        data_list += segment #sort the segments to ensure they weren't received out of order
    for x in Path('.').glob('temp*.pcap'):
        Path(x).unlink() #delete the temporary smaller files
    return data_list

""" uses the editcap command provided by Wireshark to split filename into 10000 packet pcap files
subprocess.run() will raise an exception if filename is not a pcap file """
def editcapSplit(filename):
    temp = "temp.pcap"
    command = f'editcap -c 10000 {filename} {temp}'
    subprocess.run(command, check=True, shell=True)  # split filename with editcap

# converts important data from each editcap file into a list of PacketData objects
def extractData(file):
    packets = []
    with PcapReader(file) as reader:
        for packet in reader:
            epochTimestamp = Decimal(str(packet.time))
            timestamp = sinceMidnight(epochTimestamp)
            len = packet.wirelen
            packets.append(PacketData(epochTimestamp, timestamp, len))
    return packets

""" returns number of microseconds since midnight on the day the packet arrived
used to calculate graph values later """
def sinceMidnight(epochTimestamp):
    date = datetime.datetime.fromtimestamp(epochTimestamp) #only returns time up to seconds
    seconds_midnight = datetime.datetime(date.year, date.month, date.day).timestamp()
    seconds = epochTimestamp - Decimal(seconds_midnight)
    microseconds = 1000000 * seconds
    return microseconds