from scapy.all import PcapWriter, PcapReader


# TODO Write tests
def write_packets_to_file(file_path, packet_list):
    """
    write_packets_to_file

    Write a list of packets to a pcap file in the pcaps/exported_pcaps directory

    Parameters
    output_file: the file to write the packets to
    packets: a list of packets to write to file
    """
    writer = PcapWriter(file_path, append=False, sync=True)

    for packet in packet_list:
        writer.write(packet)


def read_packets_from_file(file):
    """
    read_packets_from_file

    Read all packets from a pcap file

    Parameters
    file: the pcap file to read from

    Return
    A list containing all the packets in the file
    """
    with PcapReader(file) as reader:
        packet_list = reader.read_all()

    return packet_list
