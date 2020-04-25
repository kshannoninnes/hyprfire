# pcapconverter.py: takes in a filename for a pcap file, uses the scapy Python package to extract the data from it
# and place that data into a list of objects that will be converted to a csv format later
# Author: Dean Quaife
# Last edited: 2020/04/25

from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP
from hyprfire_app.new_scripts.packetdata import PacketData

filters = [514, 123, 53, 161] #used to filter out non TCP/UDP packets (syslog, NTP, domain, SNMP)

#main pcapconverter method; takes in a pcap filename and returns a list of Packet objects
def pcapConverter(filename):
    packets = []

    for (pkt_data, pkt_metadata,) in RawPcapReader(filename):
        ether_pkt = Ether(pkt_data)
        try:
            print(f"Values: {ether_pkt.show()}")
            ip_pkt = ether_pkt[IP]
            tcp_pkt = ip_pkt[TCP]
            ipFrom = ip_pkt.src
            ipTo = ip_pkt.dst
            portFrom = tcp_pkt.sport
            portTo = tcp_pkt.dport
            timeStamp = tcp_pkt.time
            length = ip_pkt.len - 40
            winLength = tcp_pkt.window
            tcpFlags = tcp_pkt.flags
            flags = flagFormat(tcpFlags)
            print(f"Timestamp: {timeStamp}")
            print(f"Source: {ipFrom}:{portFrom} Dest: {ipTo}:{portTo} Length: {length} Window: {winLength} Flags: {flags}")
        except IndexError:
            try: #check whether packet is a UDP packet
                ip_pkt = ether_pkt[IP]
                udp_pkt = ip_pkt[UDP]
                for port in filters: # filter packets via list. ARP, ICMP and VRRPv3 packets do not have either [TCP] or [UDP]
                    if udp_pkt.sport == port or udp_pkt.dport == port:
                        raise IndexError #stand-in for custom exception later
                ipFrom = ip_pkt.src
                ipTo = ip_pkt.dst
                portFrom = udp_pkt.sport
                portTo = udp_pkt.dport
                timeStamp = udp_pkt.time
                length = ip_pkt.len - 28
                winLength = "N/A"
                flags = "0,0,0,0,0,0,1"
                print(f"Timestamp: {timeStamp}")
                print(
                    f"Source: {ipFrom}:{portFrom} Dest: {ipTo}:{portTo} Length: {length} Window: {winLength} Flags: {flags}")
            except IndexError:
                print("that one bad")

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

def getTime(string):
    contents = string.split(".")
    seconds = int(contents[0])
    microseconds = seconds + int(contents[1])