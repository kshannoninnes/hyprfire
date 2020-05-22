import math
import logging
import subprocess
from pathlib import Path

from hyprfire_app.exceptions import EditcapException
from hyprfire_app.utils.timestamp import convert_to_editcap_format, timestamps_equal
from hyprfire_app.utils.validation import validate_file_path, validate_timestamp
import hyprfire_app.utils.pcap as ph


logger = logging.getLogger(__name__)


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
        if not Path(filtered_pcap_file).exists():
            logger.debug(f'{filtered_pcap_file} deleted')
        packet_list = self._filter_by_timestamp(filtered_list)

        logger.debug('Filtered list created')
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

        logger.debug(f'Creating pcap file with packets between "{start_sec}" and "{end_sec}"')

        temp_file = 'temp-editcapped-file.pcap'
        start = convert_to_editcap_format(start_sec)
        end = convert_to_editcap_format(end_sec)

        subprocess.run(["editcap", "-A", str(start), "-B", str(end), self.file_path, temp_file])

        if Path(temp_file).exists():
            logger.debug(f'Pcap file "{temp_file}" successfully created')

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

        logger.debug('Beginning tight filtering of packets')
        for packet in packet_list:
            if timestamps_equal(self.start_timestamp, packet.time):
                logger.debug('Initial packet found, beginning collection')
                match_found = True
            if match_found:
                filtered_list.append(packet)
            if timestamps_equal(self.end_timestamp, packet.time):
                logger.debug('Final packet found, ending collection')
                break

        if not match_found:
            logger.warning(f'No packet match found for starting timestamp "{self.start_timestamp}"')
        if len(filtered_list) == 0:
            logger.warning(f'No packets found between "{self.start_timestamp}" and "{self.end_timestamp}"')

        return filtered_list
