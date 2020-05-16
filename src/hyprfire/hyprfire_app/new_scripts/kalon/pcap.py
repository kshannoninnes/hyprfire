from pathlib import Path

from scapy.all import PcapWriter, PcapReader


# TODO Write tests
def write_packets_to_file(output_file, packet_list):
    """
    write_packets_to_file

    Write a list of packets to a pcap file

    Parameters
    output_file: the file to write the packets to
    packets: a list of packets to write to file
    """
    writer = PcapWriter(output_file, append=False, sync=True)

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


def get_pcap_files_from(path):
    """
    get_pcap_files

    Helper function to retreive a list of pcap filenames in from a directory

    Parameters
    path: a variable number of string arguments, each string being the name of a directory in the full path

    Return
    A list of pcap filenames in the directory

    Example
    Calling get_pcap_files('hyprfire_app', 'pcaps') will return all files in the path 'BASE_DIR/hyprfire_app/pcaps'
    """
    file_list = Path(path).glob('*')
    filenames = []

    for file in file_list:
        name = file.stem.lower()
        if file.is_file() and not name.startswith('.'):
            filenames.append(name)

    return filenames
