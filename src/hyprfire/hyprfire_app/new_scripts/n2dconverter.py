"""
File: n2dconverter.py
Author: Quang Le
Purpose: porting Stefan's NewBasics3.py script to turn pcap data into csv data
"""
from hyprfire_app.new_scripts.packetdata import PacketData
from hyprfire_app.new_scripts.dumpfile import Dumpfile
import hyprfire_app.new_scripts.benfordsAnalysis as ba
import hyprfire_app.new_scripts.zipfAnalysis as za
import multiprocessing as mp
import hyprfire_app.new_scripts.superthreading as st
from operator import itemgetter
import queue


def ThreadProcess(inQ, outQ, Benf, Timeo, veruficator, filename):
    # inQ = mastertuple[0]
    # outQ = mastertuple[1]
    while True:
        try:
            window = inQ.get(block=False)
            if Benf:
                if Timeo:
                    # print window
                    # print "hi"
                    times = [i[0] for i in window]
                    epochs = [i[1] for i in window]
                    intArrTimes = ba.get_interarrival_times(times)
                    benfBucks = ba.get_benfords_buckets(intArrTimes, 1)
                    uValue = ba.get_benford_u_value(benfBucks, 1)
                    timeVal = int((times[0] + times[len(window) - 1]) / 2)
                    epochVal = epochs[0]
                    tups = (timeVal, uValue, epochVal, filename, len(window))  # redundant
                    outQ.put(tups)  # redundant
                    # print tups
                else:
                    # intArrTimes = ba.GetInterArrivalTimes(window)
                    lens = [i[1] for i in window]
                    times = [i[0] for i in window]
                    epochs = [i[2] for i in window]
                    benfBucks = ba.get_benfords_buckets(lens, 1)
                    uValue = ba.get_benford_u_value(benfBucks, 1)
                    timeVal = int((times[0] + times[len(times) - 1]) / 2)
                    epochVal = epochs[0]
                    tups = (timeVal, uValue, epochVal, filename)
                    outQ.put(tups)
            else:
                if Timeo:
                    times = [i[0] for i in window]
                    epochs = [i[1] for i in window]
                    intArrTimes = ba.get_interarrival_times(times)
                    zipfBucks = za.get_zipf_buckets(intArrTimes)
                    uValue = za.get_zipf_u_value(zipfBucks)
                    timeVal = int((times[0] + times[len(window) - 1]) / 2)
                    epochVal = epochs[0]
                    tups = (timeVal, uValue, epochVal, filename)
                    outQ.put(tups)
                else:
                    # intArrTimes = ba.GetInterArrivalTimes(window)
                    lens = [i[1] for i in window]
                    times = [i[0] for i in window]
                    epochs = [i[2] for i in window]
                    zipfBucks = za.get_zipf_buckets(lens)
                    uValue = za.get_zipf_u_value(zipfBucks)
                    timeVal = int((times[0] + times[len(times) - 1]) / 2)
                    epochVal = epochs[0]
                    tups = (timeVal, uValue, epochVal, filename)
                    outQ.put(tups)
        except queue.Empty:
            if veruficator.value == 1:
                break
            pass
    # time.sleep(10)


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


def convert(dumpfile, ana_type, winsize, timelen):
    veruficator = mp.Value('i', 0)

    if ana_type == 'b':
        Benf = True
    else:
        Benf = False

    if timelen == 't':
        Timeo = True
    else:
        Timeo = False

    cores = mp.cpu_count()
    if cores > 8:
        cores = 8

    inQ = mp.Queue()
    outQ = mp.Queue()
    threadz = []

    filename = dumpfile.filename
    packets = dumpfile.packets

    # Now loading data
    for window in get_packets_window(packets, winsize):
        d = []
        if Timeo:
            d = [(packetdata.timestamp, packetdata.epochTimestamp) for packetdata in window]
        else:
            d = [(packetdata.timestamp, packetdata.len, packetdata.epochTimestamp) for packetdata in window]
        print(len(d))
        inQ.put(d)

    # Generating threads
    for i in range(0, cores):
        threadz.append(st.ThreadWorker(ThreadProcess))
    qsender = (inQ, outQ, Benf, Timeo, veruficator, filename)
    for thread in threadz:
        thread.run(qsender)

    with veruficator.get_lock():
        veruficator.value = 1
    outputlist = []

    # accumulating...")
    try:
        while True:
            outputlist.append(outQ.get(block=False))
            # print "blop"
    except Exception:
        pass
    # starting thread kill")
    inQ.cancel_join_thread()
    outQ.cancel_join_thread()
    for thread in threadz:
        thread.end()

    # sort outputlist and return to handler
    outputlist.sort(key=itemgetter(0))
    return outputlist
