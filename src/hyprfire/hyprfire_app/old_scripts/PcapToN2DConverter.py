#! /usr/bin/python3

#Advanced TCPdump segregation and data analytics tool
#Takes in a tcpd and spits out a huge file that contains metadata from said file in easy to consume csv format.
#This version has a module for stripping windows as well!
#WARNING: Your ram or your time may hate me.
#<3 Red.

#FILEFORMAT
#intarrtime,Timestamp,IPAddrFrom,IPAddrTo,PortFrom,PortTo,length,window,SYN,ACK,FIN,RST,PSH,URG,UDP

import sys
import io
import bz2
import re
import os
import time
import CSVUtils as csv
#import Queue
import multiprocessing as satan #Just a hint, this thing is literally satan. Hi Satan! :D
#import OmniAnalysis as oa
import n2dfilereader as n2df
from superthreading import threadWorker


def DataAcquisitionProc(zeQ,moo,bzMode):
    RE_IP = re.compile(".* ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) > ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*")
    RE_LEN = re.compile(".*length ([0-9]+).*")
    RE_TCPFLGS = re.compile(".*Flags (\[[\.,S,A,F,P,U,W,E,R]+\]).*")
    RE_UDP = re.compile(".*UDP.*")
    RE_WIN = re.compile(".*win ([0-9]+).*") #this is stripped from WindowStripper. It's easier than I thought it was going to be.
    prevTime = 0
    with bz2.BZ2File(str(moo) + ".n2d.prt","w") if bzMode else open(str(moo) + ".n2d.prt","w") as outF:
        while True:
            try:
                window = zeQ.get(block=False)
                #print window
                if window [0] == "DIE":
                    return
                startTime = GetTime(window[0])
                if startTime < prevTime: #this little bit deals with midnight shifts inside our long captures. Note: Don't use for more than 24 hours, this'll break
                    startTime = startTime + prevTime
                else:
                    prevTime = startTime

                for element in window:
                    try:
                        #print "match"
                        IPmatch = RE_IP.match(element)
                        LenMatch = RE_LEN.match(element)
                        flagMatch = RE_TCPFLGS.match(element)
                        winMatch = RE_WIN.match(element)


                        fromIP, toIP, fromPort, toPort = GetIPInfo(IPmatch.group(1,2))
                        #print "len"
                        length = LenMatch.group(1)
                        #print "time"
                        time = GetTime(element)
                        #print "Flags"
                        try:
                            flags = FlagProc(flagMatch.group(1))
                            leWin = winMatch.group(1)
                        except Exception as e:
                            if RE_UDP.match(element):
                                flags = "0,0,0,0,0,0,1"
                                leWin = "N/A" #Cause like there are no windows in UDP man
                            else:
                                print("ERROR",e,"PASSING UP STACK")
                                raise Exception
                        #print "write"
                        outF.write(str(time) + ',' + fromIP + ',' + toIP + ',' + fromPort + ',' + toPort + ',' + str(length) + ',' + leWin + ',' + flags + '\n')
                        #print "done"
                    except Exception as e:
#                        print("INTERNAL ERROR WITH " + str(element))
                        pass

            except Exception:
                pass

def GetTime(string):
    contents = string.split(' ')
    time = contents[0]
    timecontents = time.split(':')

    hours = int(timecontents[0])
    minutes = int(timecontents[1]) + (hours*60)
    seconds = float(timecontents[2]) + float(minutes * 60)
    microseconds = int(seconds * 1000000) #the difference could be veeery small

    return microseconds

def GetIPInfo(tupaple):
    ipset1 = tupaple[0]
    ipset2 = tupaple[1]
    iptaps1 = ipset1.split('.')
    iptaps2 = ipset2.split('.')
    ip1 = iptaps1[0] + '.' + iptaps1[1] + '.' + iptaps1[2] + '.' + iptaps1[3]
    ip2 = iptaps2[0] + '.' + iptaps2[1] + '.' + iptaps2[2] + '.' + iptaps2[3]
    port1 = iptaps1[4]
    port2 = iptaps2[4]
    return ip1,ip2,port1,port2

def FlagProc(stringz):
    SYN = 0
    ACK = 0
    FIN = 0
    RST = 0
    PSH = 0
    URG = 0
    for letter in stringz:
        if letter == 'S': SYN = 1
        if letter == 'A': ACK = 1
        if letter == 'F': FIN = 1
        if letter == 'R': RST = 1
        if letter == 'P': PSH = 1
        if letter == 'U': URG = 1
        if letter == '.': ACK = 1
    lerps = str(SYN) + ',' + str(ACK) + ',' + str(FIN) + ',' + str(RST) + ',' + str(PSH) + ',' + str(URG) + ',0'
    return lerps

def PrimaryIOThread(filename,bzMode):
    foop = n2df.FileReader(filename,999)
    cores = satan.cpu_count()
    if cores > 8:
        cores = 8
    inputQ = satan.Queue()
    threadlist = []
    print("Beginning file processing with " + str(cores) + " cores.")
    for i in range(0,cores):
        threadlist.append(threadWorker(DataAcquisitionProc))
    counter = 0
    for thread in threadlist:
        counter += 1
        thread.run((inputQ,counter,bzMode))
    for window in foop.RawGet():
        inputQ.put(window)
    time.sleep(20)
    for i in range(0,cores):
        inputQ.put(["DIE"])
    for thread in threadlist:
        thread.end()


if __name__ == '__main__':
    bzMode = csv.IsBZMode(sys.argv[1])
    PrimaryIOThread(sys.argv[1],bzMode)
    print("Now writing file")
    files = []
    for f in os.listdir("."):
        if re.search('.prt',f):
            files += [f]
    files.sort()
    csv.MergeCSVFiles(files,sys.argv[1].split('.')[0] + '.opt',0,bzMode)
    print("Merged, performing final interarrival pass...")
    with bz2.BZ2File(sys.argv[1] + ".n2d.bz2","w") if bzMode else open(sys.argv[1] + ".n2d","w") as outfile:
        with bz2.BZ2File(sys.argv[1].split('.')[0] + ".opt.bz2","r") if bzMode else open(sys.argv[1].split('.')[0] + ".opt","r") as inFile:
            #outfile.write("IntArrTime,Timestamp,IPAddrFrom,IPAddrTo,PortFrom,PortTo,length,SYN,ACK,FIN,RST,PSH,URG,UDP\n")
            prevTime = 0
            intarrtime = 0
            for line in inFile:
                time = n2df.GetN2DTime(line)
                if prevTime == 0:
                    intarrtime = 0
                else:
                    intarrtime = time - prevTime
                prevTime = time
                outfile.write(str(intarrtime) + ',' + line)
    if bzMode:
        os.remove(sys.argv[1].split('.')[0] + ".opt.bz2")
    else:
        os.remove(sys.argv[1].split('.')[0] +".opt")
    print("==Done==")
