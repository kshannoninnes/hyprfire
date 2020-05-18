from socket import getservbyport

from scapy.layers.inet import IP, TCP, UDP


# TODO Write tests
class PacketDetailsCollector:
    """
    PacketDataCollector

    PacketDataCollector is an object that takes in a single packet list, and
    collects specific details on every packet in that list.
    """

    def __init__(self, packet_list):
        """
        __init__

        Parameters
        packet_list: a list of packets to collect details on
        """
        self.packet_list = packet_list
        self.details = self._collect_details()

    def get_details(self):
        """
        get_details

        Return
        A list of dictionaries containing each packet's timestamp, category,
        source/destination ip address, and source/destination ports
        """
        return self.details

    def _collect_details(self):
        """
        _collect_details

        Collect specific details on all packets in a list

        Return
        A list of dictionaries containing each packet's timestamp, category,
        source/destination ip address, and source/destination ports
        """
        details_list = []

        for item in self.packet_list:
            packet = self._Packet(item)
            packet_data = {
                'timestamp': packet.get_timestamp(),
                'category': packet.get_category(),
                'ip_data': packet.get_ip_data(),
                'transport_data': packet.get_transport_data()
            }

            details_list.append(packet_data)

        return details_list

    class _Packet:
        """
        Packet

        Internal class used for collecting the necessary data from a packet. Used to encapsulate
        the collection process. If we need to derive data from a packet, this is where it would
        be done.
        """
        def __init__(self, packet):
            self.packet = packet
            self.UNKNOWN = 'N/A'

        def get_timestamp(self):
            """
            get_timestamp(packet)

            Return
            A string representation of the packet's timestamp
            """
            return str(self.packet.time)

        def get_category(self):
            """
            get_category

            Return
            A string representation of the packet's category
            """
            category = 'OTHER'
            if IP in self.packet:
                proto_num = self.packet[IP].proto
                category = self.packet[IP].fieldtype['proto'].i2s[proto_num]

            return category.upper()

        def get_ip_data(self):
            """
            get_ip_data

            Return
            A dictionary containing the packet's source and destination ip addresses
            """
            ip_data = {
                'src': self.UNKNOWN,
                'dst': self.UNKNOWN
            }

            if IP in self.packet:
                ip_data['src'] = self.packet[IP].src
                ip_data['dst'] = self.packet[IP].dst

            return ip_data

        def get_transport_data(self):
            """
            get_transport_data

            Return
            A dictionary containing the packet's source and destination ports
            """
            transport_data = {
                'src_port': self.UNKNOWN,
                'dst_port': self.UNKNOWN
            }

            if TCP in self.packet or UDP in self.packet:
                transport_data['src_port'] = self._resolve_port(self.packet.sport)
                transport_data['dst_port'] = self._resolve_port(self.packet.dport)

            return transport_data

        def _resolve_port(self, port_num):
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
                port_name = f'{port_num} ({self.UNKNOWN})'

            return port_name
