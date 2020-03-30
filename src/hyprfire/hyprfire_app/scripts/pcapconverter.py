# pcapconverter.py: takes in a filename for a pcap file and writes the tcpdump contents to a .tcpd file
# Author: Dean Quaife
# Last edited: 2020/03/30
import subprocess


def pcapConverter(filename):
    pcapFilename = filename + ".pcap"
    tcpdumpFilename = filename + ".tcpd"
    p = subprocess.Popen(('tcpdump', '-nnr', pcapFilename), stdout=subprocess.PIPE)
    f = open(tcpdumpFilename, 'w')
    for row in iter(p.stdout.readline, b''):
        f.write(str(row))