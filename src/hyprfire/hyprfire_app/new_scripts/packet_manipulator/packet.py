from socket import getservbyport
from scapy.layers.inet import IP, UDP, TCP

UNKNOWN = 'N/A'


def get_timestamp(packet):
    """
    _get_timestamp(packet)

    Extract the epoch timestamp from a packet

    Parameters
    packet: the packet to return a timestamp for

    Return
    A string representation of the epoch timestamp for the packet
    """
    return str(packet.time)


def get_category(packet):
    """
    _get_category

    Extract the category of a packet

    Parameters
    packet: the packet to return a category for

    Return
    A string representation of the packet's category
    """
    category = 'OTHER'
    if IP in packet:
        proto_num = packet[IP].proto
        category = packet[IP].fieldtype['proto'].i2s[proto_num]

    return category.upper()


def get_ip_data(packet):
    """
    _get_ip_data

    Get the source and destination ip addresses for a packet

    Parameters
    packet: the packet to return the ip addresses for

    Return
    A dictionary containing the source and destination ip addresses
    """
    ip_data = {
        'src': UNKNOWN,
        'dst': UNKNOWN
    }

    if IP in packet:
        ip_data['src'] = packet[IP].src
        ip_data['dst'] = packet[IP].dst

    return ip_data


def get_transport_data(packet):
    """
    _get_transport_data

    Get the source and destination ports for a packet

    Parameters
    packet: the packet to return the ports for

    Return
    A dictionary containing the source and destination ports
    """
    transport_data = {
        'src_port': UNKNOWN,
        'dst_port': UNKNOWN
    }

    if TCP in packet or UDP in packet:
        transport_data['src_port'] = _resolve_port(packet.sport)
        transport_data['dst_port'] = _resolve_port(packet.dport)

    return transport_data


def _resolve_port(port_num):
    """
    _resolve_port

    Resolve a port number to a name, if possible.

    Parameters
    port_num: an integer representing a port number

    Return
    A string representation of the port number with the associated port name.

    Note: getservbyport raises an OSError if the port number doesn't have a
    corresponding port name in the sockets library. Unfortunately, this results
    in having to use a try/except block as a form of "execution flow". This is
    really messy, but there's not much I can do to fix this as long as I use
    this function.
    """
    try:
        port_name = f'{port_num} ({getservbyport(port_num)})'
    except OSError:
        port_name = f'{port_num} ({UNKNOWN})'

    return port_name
