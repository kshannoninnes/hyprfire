# pcapconverter.py: converts packets from a pcap file into a Dumpfile object representing that file.
# pcapConverter takes a filename (with extension) and uses the PcapReader method from the Scapy library to
# extract information about each packet from the pcap file. TCP packet objects will be pieced together using
# buildTCP, and buildUDP will do the same for UDP packets. Packets besides TCP and UDP packets are filtered.
# Will raise a ConverterException if the filename doesn't exist or isn't a pcap file.
# Author: Dean Quaife
# Last edited: 2020/04/30

from scapy.utils import PcapReader, Scapy_Exception
from scapy.layers.inet import IP, TCP, UDP
from hyprfire_app.new_scripts.packetdata import PacketData
from hyprfire_app.new_scripts.dumpfile import Dumpfile
from hyprfire_app.new_scripts.converterexception import ConverterException
import datetime

# used to filter out certain packets (syslog, NTP, domain, SNMP)
filters = [514, 123, 53, 161]

#main pcapconverter method; takes in a pcap filename and returns a Dumpfile object
def pcapConverter(filename):
    packets = []
    try:
        for packet in PcapReader(filename):
            epochTimestamp = float(packet.time)
            timestamp = sinceMidnight(epochTimestamp) #used to match timestamp to Stefan's original script
            try:
                ip_pkt = packet[IP]
            except IndexError:
                continue #packets with no [IP] field such as ARP are filtered
            try:
                nextPacket = buildTCP(epochTimestamp, timestamp, ip_pkt)
                packets.append(nextPacket)
            except IndexError: #UDP, ICMP and VRRP have [UDP], not [TCP]
                if ip_pkt.proto == 1 or ip_pkt.proto == 112: #filter ICMP and VRRP via their protocol number
                    continue
                try:
                    nextPacket = buildUDP(epochTimestamp, timestamp, ip_pkt)
                except IndexError:
                    pass #filter remaining non-UDP packets
                if nextPacket is None:
                    continue #packet is one of those in the filters[] list
                packets.append(nextPacket)
    except FileNotFoundError:
        raise ConverterException("Filename does not exist")
    except Scapy_Exception:
        raise ConverterException("Filename is not a supported capture file")
    return Dumpfile(filename, packets)

#converts TCP flags returned by Scapy into a number format which is how they will be represented in the csv
#code from method FlagProc in PcapToN2DConverter by Stefan
def flagFormat(string):
    SYN = 0
    ACK = 0
    FIN = 0
    RST = 0
    PSH = 0
    URG = 0
    for letter in string:
        if letter == 'S': SYN = 1
        if letter == 'A': ACK = 1
        if letter == 'F': FIN = 1
        if letter == 'R': RST = 1
        if letter == 'P': PSH = 1
        if letter == 'U': URG = 1
    flags = str(SYN) + ',' + str(ACK) + ',' + str(FIN) + ',' + str(RST) + ',' + str(PSH) + ',' + str(URG) + ',0'
    return flags

#returns number of microseconds since midnight on the day the packet arrived; matches Stefan's original script
def sinceMidnight(epochTimestamp):
    date = datetime.datetime.fromtimestamp(epochTimestamp)
    hours = date.hour
    minutes = date.minute + 60 * hours
    seconds = date.second + 60 * minutes
    microseconds = date.microsecond + 1000000 * seconds
    return microseconds

#builds a TCP packet; returns a PacketData object
def buildTCP(epochTimestamp, timestamp, ip_pkt):
    tcp_pkt = ip_pkt[TCP]
    ipFrom = ip_pkt.src
    ipTo = ip_pkt.dst
    portFrom = tcp_pkt.sport
    portTo = tcp_pkt.dport
    length = ip_pkt.len - 40
    winLen = tcp_pkt.window
    tcpFlags = tcp_pkt.flags
    flags = flagFormat(tcpFlags)
    return PacketData(epochTimestamp, timestamp, ipFrom, ipTo, portFrom, portTo, length, winLen, flags)

#builds a UDP packet; returns a PacketData object or None if the port filter is triggered
def buildUDP(epochTimestamp, timestamp, ip_pkt):
    udp_pkt = ip_pkt[UDP]
    for port in filters:  # filter UDP packets via list
        if udp_pkt.sport == port or udp_pkt.dport == port:
                return None
    ipFrom = ip_pkt.src
    ipTo = ip_pkt.dst
    portFrom = udp_pkt.sport
    portTo = udp_pkt.dport
    length = ip_pkt.len - 28
    winLen = "N/A"  #no windows in UDP!
    flags = "0,0,0,0,0,0,1" #no flags either
    return PacketData(epochTimestamp, timestamp, ipFrom, ipTo, portFrom, portTo, length, winLen, flags)