from pathlib import Path
from decimal import Decimal
from datetime import datetime, timedelta
from scapy.all import PcapReader, PcapWriter
from hyprfire_app.utils.misc import floats_equal, PCAP_DIR, EXPORTED_PCAP_DIR
import subprocess


def _collect_packets(filename, start_timestamp, end_timestamp):
    """
    collect_packets

    Collect all packets from a file with an epoch time between start_timestamp and end_timestamp

    Parameters
    filename: the file to search
    start_timestamp: decimal unix timestamp of the first packet
    end_timestamp: decimal unix timestamp of the last packet

    Return
    A list of all packets from the start_timestamp to the end_timestamp
    """

    packet_list = []
    matching_started = False

    with PcapReader(filename) as reader:
        for packet in reader:

            # In scapy, packet.time is stored as a float. Due to precision issues with floats (represented in binary)
            # the time is converted to a string (to preserve the exact timestamp), and then converted to a decimal
            # (for comparison purposes)
            packet_timestamp = Decimal(str(packet.time))

            if floats_equal(start_timestamp, packet_timestamp):
                matching_started = True

            if matching_started:
                packet_list.append(packet)

            if floats_equal(end_timestamp, packet_timestamp):
                break

    return packet_list


# TODO Move path stuff out to base function
def _slice_with_editcap(input_file, start, end, output_file):
    """
    _slice_with_editcap

    Cuts a pcap file down to only packets contained within the range of start:end
    Note: Minimum range of 1s is enforced

    Parameters
    filename: file to slice
    start: start unix timestamp
    end: end unix timestamp

    Returns
    A string path for the output file
    """

    # editcap requires timestamps in the format of "YYYY-MM-DD hh:mm:ss"
    ec_start = datetime.fromtimestamp(start)
    ec_end = datetime.fromtimestamp(end)

    # editcap can only capture packets with a 1s gap (eg. 16:47:24 - 16:47:24 will result in an empty file)
    if abs(start - end) < 1:
        ec_end += timedelta(seconds=1)

    editcap_command = f'editcap -A "{ec_start}" -B "{ec_end}" "{input_file}" "{output_file}"'

    subprocess.call(editcap_command)


def _write_packets_to_file(path, packets):
    """
    write_packets_to_file

    Write a list of packets to a pcap file

    Parameters
    path: the file to write the packets to
    packets: a list of packets to write to file
    """
    writer = PcapWriter(path, append=False, sync=True)

    for packet in packets:
        writer.write(packet)


def _validate_timestamps(start, end):
    """
    _validate_timestamps

    A valid timestamp is a decimal greater than 0.0 (the epoch)

    Parameters
    start: the start decimal timestamp
    end: the end decimal timestamp

    Return
    boolean indicating timestamp validity
    """

    return end > start > 0


def export_packets(file_path, start_timestamp, end_timestamp):
    """
    export_packets

    Public interface for exporting packets to a file

    Parameters
    file_path: string path to an existing pcap file
    timestamp: a unique seconds-based epoch timestamp to identify the starting packet
    num_packets: number of packets to export, including the initial packet matching the timestamp

    Return
    the path to the exported file

    Raises
    ValueError if the timestamps are invalid
    IOError if there's an issue reading the file
    """
    dec_start = start_timestamp
    dec_end = end_timestamp
    filename = Path(file_path).stem

    if _validate_timestamps(dec_start, dec_end):

        temp_output_file = str(EXPORTED_PCAP_DIR / f'{filename}-editcapped.pcap')
        _slice_with_editcap(file_path, dec_start, dec_end, temp_output_file)
        packet_list = _collect_packets(temp_output_file, dec_start, dec_end)

        final_output_file = str(EXPORTED_PCAP_DIR / f'{filename}-filtered.pcap')
        _write_packets_to_file(final_output_file, packet_list)

        redundant_file = Path(temp_output_file)
        redundant_file.unlink()

        return final_output_file
    else:
        raise ValueError('Invalid time range: start_timestamp must be after the unix epoch and before end_timestamp')
