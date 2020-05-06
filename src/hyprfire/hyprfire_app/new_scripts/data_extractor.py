from scapy.all import PcapReader
from scapy.layers.inet import TCP, UDP, IP
from socket import getservbyport

from hyprfire_app.utils.misc import PCAP_DIR, EXPORTED_PCAP_DIR


def get_data(filename):
    packet_data_list = []
    count = 0

    with PcapReader(str(PCAP_DIR / filename)) as reader:
        for packet in reader:
            count += 1
            packet_data_list.append(_get_protocol(packet))

    return packet_data_list


def _get_protocol(packet):
    packet_display_data = {
        'timestamp': _get_timestamp(packet),
        'category': _get_type(packet),
        'ip_data': _get_ip_data(packet),
        'transport_data': _get_transport_data(packet)
    }

    return packet_display_data


def _get_timestamp(packet):
    return str(packet.time)


def _get_type(packet):
    category = 'OTHER'
    if IP in packet:
        proto_num = packet[IP].proto
        category = packet[IP].fieldtype['proto'].i2s[proto_num]

    return category.upper()


def _get_ip_data(packet):

    ip_data = {
        'src': 'N/A',
        'dst': 'N/A'
    }

    if IP in packet:
        ip_data['src'] = packet[IP].src
        ip_data['dst'] = packet[IP].dst

    return ip_data


def _get_transport_data(packet):

    transport_data = {
        'src_port': 'N/A',
        'dst_port': 'N/A'
    }

    if TCP in packet or UDP in packet:
        transport_data['src_port'] = _resolve_port(packet.sport)
        transport_data['dst_port'] = _resolve_port(packet.dport)

    return transport_data


def _resolve_port(port_num):
    try:
        port_name = f'{port_num} ({getservbyport(port_num)})'
    except OSError:
        port_name = str(port_num)

    return port_name
