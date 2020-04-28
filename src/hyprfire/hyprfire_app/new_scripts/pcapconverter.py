# pcapconverter.py: takes in a filename for a pcap file, uses the scapy Python package to extract the data from it
# and place that data into a list of objects that will be converted to a csv format later
# Author: Dean Quaife
# Last edited: 2020/04/25

from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP
from hyprfire_app.new_scripts.packetdata import PacketData

filters = [514, 123, 53, 161] #used to filter out non TCP/UDP packets (syslog, NTP, domain, SNMP)

#main pcapconverter method; takes in a pcap filename and returns a list of PacketData objects
def pcapConverter(filename):
    packets = []

    for (pkt_data, pkt_metadata,) in RawPcapReader(filename):
        ether_pkt = Ether(pkt_data)
        try:
            ip_pkt = ether_pkt[IP]
            tcp_pkt = ip_pkt[TCP]
            timestamp = ether_pkt.time * 1000000 #convert to microseconds; difference between packets is VERY small
            ipFrom = ip_pkt.src
            ipTo = ip_pkt.dst
            portFrom = tcp_pkt.sport
            portTo = tcp_pkt.dport
            length = ip_pkt.len - 40
            winLen = tcp_pkt.window
            tcpFlags = tcp_pkt.flags
            flags = flagFormat(tcpFlags)
            packet = PacketData(timestamp, ipFrom, ipTo, portFrom, portTo, length, winLen, flags)
            packets.append(packet)
        except IndexError:
            try: #check whether packet is a UDP packet before ignoring it
                ip_pkt = ether_pkt[IP]
                udp_pkt = ip_pkt[UDP]
                for port in filters: #filter packets via list. ARP, ICMP and VRRPv3 packets do not have either [TCP] or [UDP]
                    if udp_pkt.sport == port or udp_pkt.dport == port:
                        raise IndexError
                timestamp = ether_pkt.time * 1000000
                ipFrom = ip_pkt.src
                ipTo = ip_pkt.dst
                portFrom = udp_pkt.sport
                portTo = udp_pkt.dport
                length = ip_pkt.len - 28
                winLen = "N/A" #no windows in UDP!
                flags = "0,0,0,0,0,0,1"
                packet = PacketData(timestamp, ipFrom, ipTo, portFrom, portTo, length, winLen, flags)
                packets.append(packet)
            except IndexError: #filter
                pass
    return packets

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