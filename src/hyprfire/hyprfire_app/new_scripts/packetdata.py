#packetdata.py: contains class information for a TCP/UDP packet
#Will be used in pcapconverter to represent each packet and be passed to n2dconverter
#Author: Dean Quaife
#Last edited: 2020/04/17

#represents a TCP/UDP packet
class PacketData:
    def __init__(self, timestamp, IPFrom, IPTo, portFrom, portTo, len, flags):
        self.timestamp = timestamp
        self.IPFrom = IPFrom
        self.IPTo = IPTo
        self.portFrom = portFrom
        self.portTo = portTo
        self.len = len
        self.flags = flags