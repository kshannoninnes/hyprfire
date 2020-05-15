from scapy.utils import PcapWriter

from hyprfire_app.new_scripts.packet_manipulator.packet import get_timestamp, get_category, get_ip_data, \
    get_transport_data
from hyprfire_app.utils.misc import floats_equal


def collect_packets(large_packet_list, start_timestamp, end_timestamp):
    """
    _collect_packets

    Collect all packets from a file with an epoch time between start_timestamp and end_timestamp

    Parameters
    filename: the file to search
    start_timestamp: a unique seconds-based epoch timestamp to identify the first packet
    end_timestamp: a unique seconds-based epoch timestamp to identify the last packet

    Return
    A list of all packets from the start_timestamp to the end_timestamp
    """

    small_packet_list = []
    match_found = False

    for packet in large_packet_list:
        if floats_equal(start_timestamp, packet.time):
            match_found = True
        if match_found:
            small_packet_list.append(packet)
        if floats_equal(end_timestamp, packet.time):
            break

    return small_packet_list


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


def get_packet_data(packet_list):
    """
    get_packet_data

    Collect specific data on all packets in a pcap file

    Parameters
    file_path: full path to a pcap file

    Return
    A list of dictionaries containing each packet's timestamp, category, and source/destination ip addresses and ports
    """
    packet_data_list = []

    for packet in packet_list:
        packet_data = {
            'timestamp': get_timestamp(packet),
            'category': get_category(packet),
            'ip_data': get_ip_data(packet),
            'transport_data': get_transport_data(packet)
        }

        packet_data_list.append(packet_data)

    return packet_data_list
