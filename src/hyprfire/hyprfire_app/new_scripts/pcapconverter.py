# pcapconverter.py: converts packets from a pcap file into a list of PacketData objects
# representing that file.
# pcapConverter takes a filename (with extension) and uses the PcapReader method from the Scapy library to
# extract information about each packet from the pcap file. ExtractData does the actual work.
# Will raise a ConverterException if the filename doesn't exist or isn't a pcap file.
# Author: Dean Quaife
# Last edited: 2020/05/15

from scapy.all import PcapReader, Scapy_Exception
from hyprfire_app.new_scripts.packetdata import PacketData
from decimal import Decimal
from hyprfire_app.new_scripts.converterexception import ConverterException
import datetime

#main pcapconverter method; takes in a pcap filename and returns a PacketData list
def pcapConverter(filename):
    try:
        dataList = []
        for packet in PcapReader(filename):
            dataList.append(extractData(packet))
    except FileNotFoundError:
        raise ConverterException("Filename does not exist")
    except Scapy_Exception:
        raise ConverterException("Filename is not a supported capture file")
    return dataList

#converts important data from each packet into a PacketData object
def extractData(packet):
    epochTimestamp = Decimal(str(packet.time))
    timestamp = sinceMidnight(epochTimestamp)  # used to match timestamp to Stefan's original script
    len = packet.wirelen
    return PacketData(epochTimestamp, timestamp, len)

#returns number of microseconds since midnight on the day the packet arrived; matches Stefan's original script
def sinceMidnight(epochTimestamp):
    date = datetime.datetime.fromtimestamp(epochTimestamp)
    hours = date.hour
    minutes = date.minute + 60 * hours
    seconds = date.second + 60 * minutes
    microseconds = date.microsecond + 1000000 * seconds
    return microseconds