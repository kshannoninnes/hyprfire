"""
File: packetdata_converter.py
Author: Quang Le
Purpose: Convert list of PacketData objects from pcapconverter.py into csv values that will be used in plot_csvdata.py
to produce an anomaly graph. Based on Stefan's original NewBasics3.py script
"""

import hyprfire_app.new_scripts.benfords_analysis as ba
import hyprfire_app.new_scripts.zipf_analysis as za


def thread_process(window, output, is_benfords, is_time):
    """

        Descriptions: This is where the selected analysis types are used on a window size of PacketData
        objects to calculate values which are converted to a csv string and added to a list

        Parameters:
            window (list): a list containing a window size of PacketData objects
            output (list): a list to store the resulting strings of csv values from each window
            is_benfords (boolean): True if benfords analysis is selected, otherwise False
            is_time (boolean): True if time analysis is selected, otherwise False

        """
    if is_benfords:
        if is_time:
            # calculates using benfords and time analysis
            times = []
            epochs = []
            for i in window:
                times.append(i[0])
                epochs.append(i[1])
            int_arr_times = ba.get_interarrival_times(times)
            benf_bucks = ba.get_benfords_buckets(int_arr_times, 1)
            u_value = ba.get_benfords_u_value(benf_bucks, 1)
            time_val = int((times[0] + times[len(times) - 1]) / 2)
            start = epochs[0]
            end = epochs[len(epochs) - 1]
            csv = str(time_val) + ',' + str(u_value) + ',' + str(start) + ',' + str(end) + '\n'
            output.append(csv)
        else:
            # calculates using benfords and length analysis
            times = []
            lens = []
            epochs = []
            for i in window:
                times.append(i[0])
                lens.append(i[1])
                epochs.append(i[2])
            benf_bucks = ba.get_benfords_buckets(lens, 1)
            u_value = ba.get_benfords_u_value(benf_bucks, 1)
            time_val = int((times[0] + times[len(times) - 1]) / 2)
            start = epochs[0]
            end = epochs[len(epochs) - 1]
            csv = str(time_val) + ',' + str(u_value) + ',' + str(start) + ',' + str(end) + '\n'
            output.append(csv)
    else:
        if is_time:
            # calculates using zipf and time analysis
            times = []
            epochs = []
            for i in window:
                times.append(i[0])
                epochs.append(i[1])
            int_arr_times = ba.get_interarrival_times(times)
            zipf_bucks = za.get_zipf_buckets(int_arr_times)
            u_value = za.get_zipf_u_value(zipf_bucks)
            time_val = int((times[0] + times[len(times) - 1]) / 2)
            start = epochs[0]
            end = epochs[len(epochs) - 1]
            csv = str(time_val) + ',' + str(u_value) + ',' + str(start) + ',' + str(end) + '\n'
            output.append(csv)
        else:
            # calculates using zipf and length analysis
            times = []
            lens = []
            epochs = []
            for i in window:
                times.append(i[0])
                lens.append(i[1])
                epochs.append(i[2])
            zipf_bucks = za.get_zipf_buckets(lens)
            u_value = za.get_zipf_u_value(zipf_bucks)
            time_val = int((times[0] + times[len(times) - 1]) / 2)
            start = epochs[0]
            end = epochs[len(epochs) - 1]
            csv = str(time_val) + ',' + str(u_value) + ',' + str(start) + ',' + str(end) + '\n'
            output.append(csv)


def get_packets_window(packets, winsize):
    """

    Description: iterate over a list of PacketData objects and return a window size of those objects

    Parameters:
        packets: list of PacketData objects
        winsize: the specified window size

    Returns:
        packets_win (list): the windowsize of PacketData objects

    """

    packets_win = []
    counter = 0
    for packet in packets:
        packets_win.append(packet)
        counter += 1
        if counter == winsize:
            yield packets_win
            packets_win = []
            counter = 0


def check_arguments(packet_data, ana_type, winsize, timelen):
    """

    Description: checks the arguments passed in to convert_to_csv for value and type errors and raise them

    Parameters:
        packet_data (list): a list of PacketData objects
        ana_type (char): the type of analysis selected by the user; 'b' for benfords or 'z' for zipf
        winsize (int): the window size selected by the user
        timelen (char): another type of analysis selected by the user; 't' for time or 'l' for length

    """

    valid_ana_types = ['b', 'z']
    valid_timelen = ['t', 'l']
    if isinstance(ana_type, str):
        if ana_type not in valid_ana_types:
            raise ValueError("Invalid ana_type value: must be 'b' or 'z'")
    else:
        raise TypeError("Invalid argument type: ana_type must be a string")

    if isinstance(timelen, str):
        if timelen not in valid_timelen:
            raise ValueError("Invalid timelen value: must be 't' or 'l'")
    else:
        raise TypeError("Invalid argument type: timelen must be a string")

    if isinstance(winsize, int):
        if winsize <= 0:
            raise ValueError("Invalid winsize value: must be > 0")
    else:
        raise TypeError("Invalid argument type: winsize must be an int")

    if isinstance(packet_data, list):
        if len(packet_data) == 0:
            raise ValueError("Invalid packet_data value: list is empty")
    else:
        raise TypeError("Invalid argument type: packet_data must be a list")


def convert_to_csv(packet_data, ana_type, winsize, timelen):
    """

    Description: Takes in a list of PacketData objects and the configuration options, runs a window size of those
    objects through the selected analysis type and outputs a list of comma separated values

    Parameters:
        packet_data (list): a list of PacketData objects
        ana_type (char): the type of analysis selected by the user; 'b' for benfords or 'z' for zipf
        winsize (int): the window size selected by the user
        timelen (char): another type of analysis selected by the user; 't' for time or 'l' for length

    Returns:
        csv_str_list (list): a list of comma separated values

    """

    # Checks the arguments passed are valid
    check_arguments(packet_data, ana_type, winsize, timelen)

    if ana_type == 'b':
        is_benfords = True
    else:
        is_benfords = False

    if timelen == 't':
        is_time = True
    else:
        is_time = False

    out_str = []
    # Pass windowsize of packet data into thread_process for processing
    for window in get_packets_window(packet_data, winsize):
        d = []
        if is_time:
            d = [(packetdata.timestamp, packetdata.epochTimestamp) for packetdata in window]
        else:
            d = [(packetdata.timestamp, packetdata.len, packetdata.epochTimestamp) for packetdata in window]
        thread_process(d, out_str, is_benfords, is_time)

    return out_str
