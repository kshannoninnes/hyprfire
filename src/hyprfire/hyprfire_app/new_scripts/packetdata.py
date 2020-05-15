# packetdata.py: contains class information for a packet
# Will be used in pcapconverter to represent each packet and be passed to n2dconverter
# Author: Dean Quaife
# Last edited: 2020/05/15

#represents a packet
class PacketData:
    def __init__(self, epochTimestamp, timestamp, len):
        self.epochTimestamp = epochTimestamp
        self.timestamp = timestamp #this value is microseconds since midnight on day of capture
        self.len = len

    #required for comparing packets in testing
    def __eq__(self, other):
        if not isinstance(other, PacketData):
            return NotImplemented
        return self.__dict__ == other.__dict__