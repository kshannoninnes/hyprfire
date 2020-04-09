"""
File: n2dconverter.py
Author: Quang Le
Purpose: porting Stefan's NewBasics3.py script to turn n2d data into csv data
"""
import benfordsAnalysis as ba
import zipfAnalysis as za
import argparse
import n2dfilereader as n2df
import multiprocessing as mp
import superthreading as st
import time
import bz2
from operator import itemgetter
import sys
import queue

def ThreadProcess(inQ,outQ,Benf,Timeo,veruficator):
    #inQ = mastertuple[0]
    #outQ = mastertuple[1]
    while True:
        try:
            window = inQ.get(block=False)
            if Benf:
                if Timeo:
                    #print window
                    #print "hi"
                    intArrTimes = ba.GetInterArrivalTimes(window)
                    benfBucks = ba.GetBenfordsBuckets(intArrTimes,1)
                    uValue = ba.GetBenfordU(benfBucks,1)
                    timeVal = int((window[0] + window[len(window)-1])/2)
                    tups = (timeVal,uValue)
                    outQ.put(tups)
                    #print tups
                else:
                    #intArrTimes = ba.GetInterArrivalTimes(window)
                    lens = [i[1] for i in window]
                    times = [i[0] for i in window]
                    benfBucks = ba.GetBenfordsBuckets(lens,1)
                    uValue = ba.GetBenfordU(benfBucks,1)
                    timeVal = int((times[0] + times[len(times)-1])/2)
                    tups = (timeVal,uValue)
                    outQ.put(tups)
            else:
                if Timeo:
                    intArrTimes = ba.GetInterArrivalTimes(window)
                    zipfBucks = za.GetZipfBuckets(intArrTimes)
                    uValue = za.GetZipfU(zipfBucks)
                    timeVal = int((window[0] + window[len(window)-1])/2)
                    tups = (timeVal,uValue)
                    outQ.put(tups)
                else:
                    #intArrTimes = ba.GetInterArrivalTimes(window)
                    lens = [i[1] for i in window]
                    times = [i[0] for i in window]
                    zipfBucks = za.GetZipfBuckets(lens)
                    uValue = za.GetZipfU(zipfBucks)
                    timeVal = int((times[0] + times[len(times)-1])/2)
                    tups = (timeVal,uValue)
                    outQ.put(tups)
        except queue.Empty:
            if veruficator.value == 1:
                break
            pass
    #time.sleep(10)

#Currently converts n2d file instead of n2d data as format of data is not known yet
def convert (n2ddata, anaType, winsize, timelen):
    veruficator = mp.Value('i',0)

    if anaType == 'b':
        Benf = True
    else:
        Benf = False

    if timelen == 't':
        Timeo = True
    else:
        Timeo = False

    windowsize = winsize
    filereader = n2df.FileReader(n2ddata, windowsize)
    cores = mp.cpu_count()

    if cores > 8:
        cores = 8

    inQ = mp.Queue()
    outQ = mp.Queue()
    threadz = []
    #Generating threads
    for i in range(0,cores):
        threadz.append(st.threadWorker(ThreadProcess))
    qsender = (inQ,outQ,Benf,Timeo,veruficator)
    for thread in threadz:
        thread.run(qsender)
    #Now loading data
    for window in filereader.Get():
        d = []
        if args.timelen == '+t':
            d = [int(x[1]) for x in window]
        else:
            d = [(int(x[1]),int(x[6])) for x in window]
        #print len(d)
        inQ.put(d)

    with veruficator.get_lock():
        veruficator.value = 1
    outputlist = []

    #accumulating...")
    try:
        while True:
            outputlist.append(outQ.get(block=False))
            #print "blop"
    except Exception:
        pass
    #starting thread kill")
    inQ.cancel_join_thread()
    outQ.cancel_join_thread()
    for thread in threadz:
        thread.end()

    #sort outputlist and return to handler
    outputlist.sort(key=itemgetter(0))
    return outputlist