from scapy.all import PcapReader
from pathlib import Path
from socket import getservbyport

from scapy.layers.inet import TCP, IP

root_dir = Path(__file__).parent.parent.parent
input_dir = Path(root_dir / 'pcaps')
output_dir = Path(input_dir / 'exported_pcaps')


def get_data(filename):
    packet_data_list = []

    with PcapReader(str(input_dir / filename)) as reader:
        for packet in reader:
            packet_data_list.append(_get_protocol(packet))

    return packet_data_list


def _get_protocol(packet):
    # Set variables to the same default value
    packet_display_data = {
        'protocol': 'N/A',
        'src_ip': 'N/A',
        'dst_ip': 'N/A',
        'src_port': 'N/A',
        'dst_port': 'N/A',
        'src_port_name': 'N/A',
        'dst_port_name': 'N/A'
    }

    if IP in packet:
        packet_display_data['protocol'] = packet[IP].proto
        packet_display_data['src_ip'] = packet[IP].src
        packet_display_data['dst_ip'] = packet[IP].dst

    if TCP in packet:
        packet_display_data['src_port'] = packet[TCP].sport
        packet_display_data['dst_port'] = packet[TCP].dport
        packet_display_data['src_port_name'] = _get_port_name(packet_display_data['src_port'])
        packet_display_data['dst_port_name'] = _get_port_name(packet_display_data['dst_port'])

    return packet_display_data


def _get_port_name(port_num):
    try:
        port_name = getservbyport(port_num)
    except OSError:
        port_name = 'N/A'

    return port_name
