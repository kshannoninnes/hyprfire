from pathlib import Path
from datetime import datetime
from scapy.all import PcapReader, PcapWriter
from hyprfire_app.utils.misc import floats_equal, EXPORTED_PCAP_DIR
import subprocess


def export_packets_in_range(file_path, start_timestamp, end_timestamp):
    """
    export_packets_in_range

    Export all packets between a start and end timestamp to a new file

    Parameters
    file_path: string path to an existing pcap file
    start_timestamp: a unique seconds-based epoch timestamp to identify the first packet
    end_timestamp: a unique seconds-based epoch timestamp to identify the last packet

    Return
    String representation of the path to the newly created file

    Raises
    ValueError:     if the timestamps are invalid
    IOError:        if there's an issue reading the file
    """
    filename = Path(file_path).stem

    if _validate_timestamps(start_timestamp, end_timestamp):

        temp_output_file = str(EXPORTED_PCAP_DIR / f'{filename}-editcapped.pcap')
        _slice_with_editcap(file_path, start_timestamp, end_timestamp, temp_output_file)
        packet_list = _collect_packets(temp_output_file, start_timestamp, end_timestamp)

        final_output_file = str(EXPORTED_PCAP_DIR / f'{filename}-filtered.pcap')
        _write_packets_to_file(final_output_file, packet_list)

        redundant_file = Path(temp_output_file)
        redundant_file.unlink()

        return final_output_file
    else:
        raise ValueError('Invalid time range: start_timestamp must be after the unix epoch and before end_timestamp')


def _collect_packets(filename, start_timestamp, end_timestamp):
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

    packet_list = []
    matching_started = False

    with PcapReader(filename) as reader:
        for packet in reader:

            if floats_equal(start_timestamp, packet.time):
                matching_started = True

            if matching_started:
                packet_list.append(packet)

            if floats_equal(end_timestamp, packet.time):
                break

    return packet_list


def _slice_with_editcap(input_file, start_timestamp, end_timestamp, output_file):
    """
    _slice_with_editcap

    Cuts a pcap file down to only packets contained within the range of start:end
    Note: Editcap requires a minimum of 1s difference between the two timestamps

    Parameters
    filename: the file to slice
    start_timestamp: a unique seconds-based epoch timestamp to identify the first packet
    end_timestamp: a unique seconds-based epoch timestamp to identify the last packet
    output_file: the file to write to
    """
    # editcap can only capture packets with a 1s gap (eg. 16:47:24 - 16:47:24 will result in an empty file)
    if abs(start_timestamp - end_timestamp) < 1:
        end_timestamp += 1

    # editcap requires timestamps in the format of "YYYY-MM-DD hh:mm:ss"
    formatted_start = datetime.fromtimestamp(start_timestamp)
    formatted_end = datetime.fromtimestamp(end_timestamp)

    editcap_command = f'editcap -A "{formatted_start}" -B "{formatted_end}" "{input_file}" "{output_file}"'

    subprocess.call(editcap_command)


def _write_packets_to_file(output_file, packet_list):
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


def _validate_timestamps(start_timestamp, end_timestamp):
    """
    _validate_timestamps

    A valid timestamp is a decimal greater than 0.0 (the epoch)

    Parameters
    start_timestamp: a unique seconds-based epoch timestamp to identify the first packet
    end_timestamp: a unique seconds-based epoch timestamp to identify the last packet

    Return
    boolean indicating timestamp validity
    """

    return end_timestamp > start_timestamp > 0
