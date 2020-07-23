""" packetdata.py: contains class information for a packet
Will be used in pcapconverter to represent each packet and be passed to packdata_converter
Author: Dean Quaife
Last edited: 2020/05/21
"""

#represents a packet
class PacketData:
    def __init__(self, epochTimestamp, timestamp, len):
        self.epochTimestamp = epochTimestamp
        self.timestamp = timestamp #this value is microseconds since midnight on day of capture
        self.len = len