# pcapconverter.py: takes in a filename for a pcap file, runs the tcpdump command on it and stores the output
# in a list, which it returns
# Author: Dean Quaife
# Last edited: 2020/04/08
import subprocess


def pcapConverter(filename):
    packets = []

    p = subprocess.Popen(('tcpdump', '-nnlr', filename), stdout=subprocess.PIPE)
    for row in iter(p.stdout.readline, b''):
        packets.append(row) #this is slow. may need to implement multiprocessing

    return packets