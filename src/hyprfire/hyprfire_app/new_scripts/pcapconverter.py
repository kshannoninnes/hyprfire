# pcapconverter.py: converts packets from a pcap file into a Dumpfile object representing that file.
# pcapConverter takes a filename (with extension) and uses the PcapReader method from the Scapy library to
# extract information about each packet from the pcap file. TCP packet objects will be pieced together using
# buildTCP, and buildUDP will do the same for UDP packets. Packets besides TCP and UDP packets are filtered.
# Will raise a ConverterException if the filename doesn't exist or isn't a pcap file.
# Author: Dean Quaife
# Last edited: 2020/05/07

from scapy.utils import PcapReader, Scapy_Exception
from hyprfire_app.new_scripts.packetdata import PacketData
from hyprfire_app.new_scripts.dumpfile import Dumpfile
from scapy.layers.inet import IP, TCP, UDP #required import for PcapReader to work correctly even though it isn't used
from hyprfire_app.new_scripts.converterexception import ConverterException
import datetime, multiprocessing, math

#main pcapconverter method; takes in a pcap filename and returns a Dumpfile object
def pcapConverter(filename):
    try:
        with multiprocessing.Manager() as manager:
            cores = multiprocessing.cpu_count()
            dataList = []
            packetList = []
            segList = manager.list()
            proList = []
            inputQ = multiprocessing.Queue()
            for packet in PcapReader(filename):
                packetList.append(packet)
            segmentSize = math.ceil(len(packetList)/cores)
            for i in range(0, len(packetList), segmentSize):
                inputQ.put(packetList[i:i + segmentSize])
            for i in range(cores):
                proList.append(multiprocessing.Process(target=extractData, args=(inputQ, segList)))
            for p in proList:
                p.start()
            for p in proList:
                p.join()
            for i in segList:
                dataList += i
    except FileNotFoundError:
        raise ConverterException("Filename does not exist")
    except Scapy_Exception:
        raise ConverterException("Filename is not a supported capture file")
    return dataList

def extractData(inputQ, dataList):
    segment = inputQ.get()
    packets = []
    for packet in segment:
        epochTimestamp = float(packet.time)
        timestamp = sinceMidnight(epochTimestamp)  # used to match timestamp to Stefan's original script
        len = packet.wirelen
        nextPkt = PacketData(epochTimestamp, timestamp, len)
        packets.append(nextPkt)
    dataList.append(packets)

#returns number of microseconds since midnight on the day the packet arrived; matches Stefan's original script
def sinceMidnight(epochTimestamp):
    date = datetime.datetime.fromtimestamp(epochTimestamp)
    hours = date.hour
    minutes = date.minute + 60 * hours
    seconds = date.second + 60 * minutes
    microseconds = date.microsecond + 1000000 * seconds
    return microseconds