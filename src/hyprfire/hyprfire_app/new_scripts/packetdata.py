# packetdata.py: contains class information for a TCP/UDP packet
# Will be used in pcapconverter to represent each packet and be passed to n2dconverter
# Author: Dean Quaife
# Last edited: 2020/04/27

#represents a TCP/UDP packet
class PacketData:
    def __init__(self, epochTimestamp, timestamp, IPFrom, IPTo, portFrom, portTo, len, winLen, flags):
        self.epochTimestamp = epochTimestamp
        self.timestamp = timestamp #this value is microseconds since midnight on day of capture
        self.IPFrom = IPFrom
        self.IPTo = IPTo
        self.portFrom = portFrom
        self.portTo = portTo
        self.len = len
        self.winLen = winLen
        self.flags = flags

    #required for comparing packets in testing
    def __eq__(self, other):
        if not isinstance(other, PacketData):
            return NotImplemented
        return self.__dict__ == other.__dict__