from scapy.all import RawPcapReader, PcapReader, PcapWriter
import time
from pathlib import Path

root_path = Path(__file__).parent.parent.parent
input_path = Path(root_path / 'pcaps')
output_path = Path(input_path / 'exported_pcaps')


def find_packets(filename, timestamp, num_packets):
    """
    find_packets

    Find a number of packets in a file starting from the packet which matches the timestamp provided

    Parameters
    filename: the file to search
    timestamp: a unique seconds-based epoch timestamp to identify the starting packet
    num_packets: the number of packets to collect
    """
    start = time.time()
    print('Starting search at ' + str(start))

    count = num_packets
    start_collecting = False

    for packet in PcapReader(str(input_path / filename)):
        match = timestamp.rstrip('0') == str(packet.time)
        print('Matching ' + timestamp.rstrip('0') + ' against ' + str(packet.time))
        if match:
            start_collecting = True
            print('Beginning collection of packets!')

        if start_collecting:
            packet_writer = PcapWriter(str(output_path / str(filename + '.filtered.pcap')), append=True, sync=True)
            packet_writer.write(packet)
            count = count - 1

            if count <= 0:
                break

    finished = time.time()
    print('Finished searching at ' + str(finished))
    duration = finished - start
    print('Search took ' + str(duration) + ' seconds to complete.')