'''
File: packetdata_converter.py
Author: Quang Le
Purpose: porting Stefan's NewBasics3.py script to turn pcap data into csv data
'''
import operator
import time

from hyprfire_app.new_scripts.packetdata import PacketData
from hyprfire_app.new_scripts.dumpfile import Dumpfile
import hyprfire_app.new_scripts.benfords_analysis as ba
import hyprfire_app.new_scripts.zipf_analysis as za
import multiprocessing as mp
import hyprfire_app.new_scripts.superthreading as st
import queue

'''
Class name: CSVData
This class is used to store each row of the csv as an object
'''
class CSVData:
    def __init__(self, timestamp, uvalue, start_epoch, end_epoch):
        self.timestamp = timestamp
        self.uvalue = uvalue
        self.start_epoch = start_epoch
        self.end_epoch = end_epoch



'''
Function: thread_process
Descriptions: This is where benfords or zipf algorithms are used to calculate the values needed for CSVData
Input: 
    in_q: queue of variables from each PacketData object 
    out_q: queue of CSVData objects 
    mp_value: multiprocessing value
    is_benfords: boolean, True if benfords analysis is selected
    is_time: boolean, True if time analysis is selected
    filename: name of original pcap file
'''
def thread_process(in_q, out_q, is_benfords, is_time, mp_value):
    while True:
        try:
            window = in_q.get(block=False)
            if is_benfords:
                if is_time:
                    # calculates using benfords and time analysis
                    times = [i[0] for i in window]
                    epochs = [i[1] for i in window]
                    int_arr_times = ba.get_interarrival_times(times)
                    benf_bucks = ba.get_benfords_buckets(int_arr_times, 1)
                    u_value = ba.get_benfords_u_value(benf_bucks, 1)
                    time_val = int((times[0] + times[len(times) - 1]) / 2)
                    start = epochs[0]
                    end = epochs[len(epochs) - 1]
                    csv = CSVData(time_val, u_value, start, end)
                    out_q.put(csv)
                else:
                    # calculates using benfords and length analysis
                    lens = [i[1] for i in window]
                    times = [i[0] for i in window]
                    epochs = [i[2] for i in window]
                    benf_bucks = ba.get_benfords_buckets(lens, 1)
                    u_value = ba.get_benfords_u_value(benf_bucks, 1)
                    time_val = int((times[0] + times[len(times) - 1]) / 2)
                    start = epochs[0]
                    end = epochs[len(epochs) - 1]
                    csv = CSVData(time_val, u_value, start, end)
                    out_q.put(csv)
            else:
                if is_time:
                    # calculates using zipf and time analysis
                    times = [i[0] for i in window]
                    epochs = [i[1] for i in window]
                    int_arr_times = ba.get_interarrival_times(times)
                    zipf_bucks = za.get_zipf_buckets(int_arr_times)
                    u_value = za.get_zipf_u_value(zipf_bucks)
                    time_val = int((times[0] + times[len(times) - 1]) / 2)
                    start = epochs[0]
                    end = epochs[len(epochs) - 1]
                    csv = CSVData(time_val, u_value, start, end)
                    out_q.put(csv)
                else:
                    # calculates using zipf and length analysis
                    lens = [i[1] for i in window]
                    times = [i[0] for i in window]
                    epochs = [i[2] for i in window]
                    zipf_bucks = za.get_zipf_buckets(lens)
                    u_value = za.get_zipf_u_value(zipf_bucks)
                    time_val = int((times[0] + times[len(times) - 1]) / 2)
                    start = epochs[0]
                    end = epochs[len(epochs) - 1]
                    csv = CSVData(time_val, u_value, start, end)
                    out_q.put(csv)
        except queue.Empty:
            if mp_value.value == 1:
                break
            pass


'''
Function: get_packets_window
Description: return a list of PacketData objects within a specific window size
'''
def get_packets_window(packets, winsize):
    packets_win = []
    counter = 0
    for packet in packets:
        try:
            packets_win.append(packet)
            counter += 1
            if counter == winsize:
                yield packets_win
                packets_win = []
                counter = 0
        except LookupError:
            print("Index Error Exception Raised, list index out of range")

'''
Function: dump_queue_to_list
Description: empties contents of a queue into a list and returns it
'''
def dump_queue_to_list(out_q):
    output = []
    while True:
        csv = out_q.get()
        if csv is None:
            break
        else:
            output.append(csv)
    time.sleep(.5)
    return output


'''
Function: convert_to_csv
Description: Takes in a list of PacketData objects and the configuration options, runs through the selected algorithms 
using multithreading and puts the results into CSVData objects, then it returns a sorted list of those objects 
Inputs:
    dumpfile: Dumpfile object which contains a list of PacketData objects and the filename
    ana_type: the type of analysis selected by the user; 'b' for benfords or 'z' for zipf
    winsize: the window size selected by the user
    timelen: another type of analysis selected by the user; 't' for time or 'l' for length 
Output:
    sorted_list: a sorted list of CSVData objects
'''
def convert_to_csv(packet_data, ana_type, winsize, timelen):
    # Checks the arguments passed are valid
    if ana_type == 'b':
        is_benfords = True
    elif ana_type == 'z':
        is_benfords = False
    else:
        raise ValueError(ana_type)

    if timelen == 't':
        is_time = True
    elif timelen == 'l':
        is_time = False
    else:
        raise ValueError(timelen)

    if isinstance(packet_data, list):
        packets = packet_data
    else:
        raise TypeError

    if winsize < 1:
        raise ValueError

    mp_value = mp.Value('i', 0)
    cores = mp.cpu_count()
    if cores > 8:
        cores = 8

    in_q = mp.Queue()
    out_q = mp.Queue()
    thread_list = []

    # Generating threads
    for i in range(0, cores):
        thread_list.append(st.ThreadWorker(thread_process))
    q_sender = (in_q, out_q, is_benfords, is_time, mp_value)
    for thread in thread_list:
        thread.run(q_sender)

    # Loads windowsize of packet data into the queue for processing
    for window in get_packets_window(packets, winsize):
        d = []
        if is_time:
            d = [(packetdata.timestamp, packetdata.epochTimestamp) for packetdata in window]
        else:
            d = [(packetdata.timestamp, packetdata.len, packetdata.epochTimestamp) for packetdata in window]
        # print(len(d))
        in_q.put(d)

    with mp_value.get_lock():
        mp_value.value = 1

    out_q.put(None)
    csv_list = dump_queue_to_list(out_q)

    # Starts thread kill
    in_q.cancel_join_thread()
    out_q.cancel_join_thread()
    for thread in thread_list:
        thread.end()

    # Sort csv_list and return to handler
    sorted_list = sorted(csv_list, key=operator.attrgetter("timestamp"))
    return sorted_list
