import subprocess
from pathlib import Path

from scapy.all import PcapReader

from hyprfire_app.exceptions import EditcapException
from hyprfire_app.new_scripts.packet_manipulator.timestamp import convert_to_editcap_format, validate_timestamp


def slice_with_editcap(input_file, start_second, end_second):
    """
    slice_with_editcap

    Returns a list containing only packets within the range of start_second:end_second
    Note: Editcap requires a minimum of 1s difference between the two timestamps

    Parameters
    input_file: a string representing the file path to the pcap file
    start_second: an integer representing the seconds since epoch
    end_second: an integer representing the seconds since epoch

    Return
    A list of packets
    """
    if start_second > end_second:
        raise EditcapException('Start time must be before end time')

    validate_timestamp(start_second)
    validate_timestamp(end_second)

    temp_file = 'temp-editcapped-file.pcap'
    start, end = convert_to_editcap_format(start_second, end_second)

    editcap_command = f'editcap -A "{start}" -B "{end}" "{input_file}" "{temp_file}"'
    subprocess.call(editcap_command)

    return _create_list_from(temp_file)


def _create_list_from(file):
    with PcapReader(file) as reader:
        packet_list = reader.read_all()
    Path(file).unlink()

    return packet_list
