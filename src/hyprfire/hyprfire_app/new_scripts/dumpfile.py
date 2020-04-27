# dumpfile.py: contains class information for a dumpfile object
# Author: Dean Quaife
# Last edited: 2020/04/27

#represents a pcap file as an object. used to seperate different packets for storage later
class Dumpfile:
    def __init__(self, filename, packets):
        self.filename = filename
        self.packets = packets