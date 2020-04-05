# pcapconverter.py: takes in a filename for a pcap file and writes the tcpdump contents to a .tcpd file
# Author: Dean Quaife
# Last edited: 2020/04/05
import subprocess


def pcapConverter(filename):
    pcapFilename = filename + ".pcap"
    tcpdumpFilename = filename + ".tcpd"
    cmd = "tcpdump -nnr " + pcapFilename
    #p = subprocess.Popen(('tcpdump', '-nnr', '-l', pcapFilename), stdout=subprocess.PIPE)
    with open(tcpdumpFilename, 'wb') as f:
        f.write(subprocess.check_output(cmd, shell=True))
        f.close()