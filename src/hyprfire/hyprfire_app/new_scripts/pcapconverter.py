# pcapconverter.py: takes in a filename for a pcap file, uses the scapy Python package to extract the data from it
# and place that data into a list of objects that will be converted to a csv format later
# Author: Dean Quaife
# Last edited: 2020/04/27

from scapy.utils import PcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP
from hyprfire_app.new_scripts.packetdata import PacketData
from hyprfire_app.new_scripts.dumpfile import Dumpfile
import datetime

filters = [514, 123, 53, 161] #used to filter out certain packets (syslog, NTP, domain, SNMP)

#main pcapconverter method; takes in a pcap filename and returns a list of PacketData objects
def pcapConverter(filename):
    packets = []

    for packet in PcapReader(filename):
        ether_pkt = Ether(packet)
        epochTimestamp = float(packet.time)
        timestamp = sinceMidnight(epochTimestamp)
        try:
            ip_pkt = packet[IP]
        except IndexError:
            continue #filter ARP, STP, DHCP and IPv6 packets missing relevant info
        try:
            packet = buildTCP(epochTimestamp, timestamp, ip_pkt)
            packets.append(packet)
        except IndexError: #packet is UDP, ICMP or VRRP
            if ip_pkt.proto == 1 or ip_pkt.proto == 112: #filter ICMP and VRRP
                continue
            udp_pkt = ip_pkt[UDP]
            skip = False
            for port in filters:  # filter UDP packets via list
                if udp_pkt.sport == port or udp_pkt.dport == port:
                    skip = True
            if skip:
                continue
            ipFrom = ip_pkt.src
            ipTo = ip_pkt.dst
            portFrom = udp_pkt.sport
            portTo = udp_pkt.dport
            length = ip_pkt.len - 28
            winLen = "N/A" #no windows in UDP!
            flags = "0,0,0,0,0,0,1"
            packet = PacketData(epochTimestamp, timestamp, ipFrom, ipTo, portFrom, portTo, length, winLen, flags)
            packets.append(packet)
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
        if letter == '.': ACK = 1
    flags = str(SYN) + ',' + str(ACK) + ',' + str(FIN) + ',' + str(RST) + ',' + str(PSH) + ',' + str(URG) + ',0'
    return flags

#returns number of microseconds since midnight on the day the packet arrived
def sinceMidnight(epochTimestamp):
    date = datetime.datetime.fromtimestamp(epochTimestamp)
    hours = date.hour
    minutes = date.minute + 60 * hours
    seconds = date.second + 60 * minutes
    microseconds = date.microsecond + 1000000 * seconds
    return microseconds

#builds a TCP packet
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

def buildUDP(epochTimestamp, timestamp, ip_pkt):
    udp_pkt = ip_pkt[UDP]