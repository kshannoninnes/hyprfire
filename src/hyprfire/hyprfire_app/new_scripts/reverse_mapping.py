from scapy.all import PcapReader, PcapWriter
from pathlib import Path
from decimal import Decimal


root_path = Path(__file__).parent.parent.parent
input_path = Path(root_path / 'pcaps')
output_path = Path(input_path / 'exported_pcaps')


def _collect_packets(filename, timestamp, num_packets):
    """
    collect_packets

    Find a number of packets in a file starting from the packet which matches the timestamp provided
    Note: Currently very very slow (thanks scapy -_-)

    Parameters
    filename: the file to search
    timestamp: a unique seconds-based epoch timestamp to identify the starting packet
    num_packets: the number of packets to collect

    Return
    A list of packets of size num_packets, starting from the packet with the matching timestamp
    """

    count = num_packets
    start_collecting = False
    packet_list = []

    for packet in PcapReader(str(input_path / filename)):
        match = timestamp.compare(packet.time) == 0

        if match:
            start_collecting = True

        if start_collecting:
            packet_list.append(packet)
            count = count - 1

            if count <= 0:
                break

    return packet_list


def _write_packets_to_file(path, packets):
    """
    write_packets_to_file

    Write a list of packets to a pcap file

    Parameters
    path: the file to write the packets to
    packets: a list of packets to write to file
    """
    writer = PcapWriter(path, append=True, sync=True)

    for packet in packets:
        writer.write(packet)


def export_packets(filename, timestamp, num_packets):
    """
    export_packets

    Public interface for exporting packets to a file

    Parameters
    filename: file to export packets from
    timestamp: a unique seconds-based epoch timestamp to identify the starting packet
    num_packets: number of packets to export, including the initial packet matching the timestamp

    Return
    the path to the exported file
    """
    dec_timestamp = Decimal(timestamp)
    valid = validate_timestamp(dec_timestamp) and validate_num_packets(num_packets)

    if valid:
        packets = _collect_packets(filename, dec_timestamp, num_packets)
        output_file = str(output_path / str(filename + '.filtered.pcap'))
        _write_packets_to_file(output_file, packets)

        return output_file


def validate_timestamp(timestamp):
    """
    validate_timestamp

    A valid timestamp is a decimal greater than 0.0 (the epoch)

    Parameters
    timestamp: the decimal timestamp to validate

    Return
    boolean indicating timestamp validity
    """
    if timestamp.compare(0) == 1:
        return True
    else:
        raise ValueError("Timestamp must be greater then 0.0 (the unix epoch)")


def validate_num_packets(num_packets):
    """
    validate_num_packets

    A valid number of packets is a decimal greater than 0

    Parameters
    num_packets: the number of packets

    Return
    boolean indicating whether the number of packets is valid
    """
    if num_packets > 0:
        return True
    else:
        raise ValueError("Number of packets cannot be <= 0")
