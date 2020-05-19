import math
import subprocess
from pathlib import Path

from hyprfire_app.exceptions import EditcapException
from hyprfire_app.utils.timestamp import convert_to_editcap_format, timestamps_equal
from hyprfire_app.utils.validation import validate_file_path, validate_timestamp
import hyprfire_app.utils.pcap as ph


class PacketFilter:
    """
    PacketFilter

    PacketFilter will take in a path to a pcap file, along with a start and end timestamp. It provides
    a single method to get a filtered list of packets in return.
    """

    def __init__(self, file_path, start, end):
        """
        __init__

        Parameters
        file_path: the path to the pcap file to filter packets from
        start: an epoch timestamp identifying the first packet in the filtered list
        end: an epoch timestamp identifying the last packet in the filtered list
        """
        self.file_path = validate_file_path(str(Path(file_path)))
        self.start_timestamp = validate_timestamp(start)
        self.end_timestamp = validate_timestamp(end)

        self.filtered_list = self._filter_packets()

    def get_filtered_list(self):
        """
        get_filtered_list

        Return
        The filtered packet list
        """
        return self.filtered_list

    def _filter_packets(self):
        """
        _filter_packets

        Filter packets from the provided file into a list containing only packets
        between the start and end timestamp

        Return
        A list of filtered packets
        """
        filtered_pcap_file = self._create_filtered_pcap()
        filtered_list = ph.read_packets_from_file(filtered_pcap_file)
        Path(filtered_pcap_file).unlink()
        packet_list = self._filter_by_timestamp(filtered_list)

        return packet_list

    def _create_filtered_pcap(self):
        """
        _create_filtered_pcap

        Create a temporary pcap file containing only packets loosely filtered between a
        start and end timestamp

        Return
        The path to the temporary pcap file
        """
        start_sec = int(math.floor(self.start_timestamp))
        end_sec = int(math.ceil(self.end_timestamp))

        if start_sec > end_sec:
            raise EditcapException('Start time must be before end time')

        temp_file = 'temp-editcapped-file.pcap'
        start = convert_to_editcap_format(start_sec)
        end = convert_to_editcap_format(end_sec)

        editcap_command = f'editcap -A "{start}" -B "{end}" "{self.file_path}" "{temp_file}"'
        subprocess.call(editcap_command, shell=True)

        return temp_file

    def _filter_by_timestamp(self, packet_list):
        """
        _filter_by_timestamp

        Take in a loosely filtered list of packets and return a tightly filtered list of packets

        Parameters
        packet_list: a list of packets to filter

        Return
        A tightly filtered list of packets
        """
        filtered_list = []
        match_found = False

        for packet in packet_list:
            if timestamps_equal(self.start_timestamp, packet.time):
                match_found = True
            if match_found:
                filtered_list.append(packet)
            if timestamps_equal(self.end_timestamp, packet.time):
                break

        return filtered_list
