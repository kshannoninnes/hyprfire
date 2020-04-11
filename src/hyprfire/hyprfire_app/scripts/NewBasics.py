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
import Queue


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
		except Queue.Empty:
			if veruficator.value == 1:
				break
			pass
	#time.sleep(10)
	print "closing up shop"



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Analyses an n2d file using either Benford\'s or Zipf\'s law')
	parser.add_argument('file',type=str, help='File to analyse. Should be ndmp.')
	parser.add_argument('anaType',type=str,choices=('+b','+z'), help='Benfords or Zipf')
	parser.add_argument('--win',type=int,default=999,help='Window size')
	#parser.add_argument('--output',default='output.txt',help='Output file name')
	parser.add_argument('timelen',type=str,choices=('+t','+l'),help='time analysis or length analysis')

	args = parser.parse_args()
	
	veruficator = mp.Value('i',0)

	if args.anaType == '+b':
		Benf = True
	else:
		Benf = False


	if args.timelen == '+t':
		Timeo = True
	else:
		Timeo = False
	windowsize = args.win

	filereader = n2df.FileReader(args.file,windowsize)

	cores = mp.cpu_count()

	inQ = mp.Queue()
	outQ = mp.Queue()
	threadz = []
	print "Generating " + str(cores) + " threads"
	for i in range(0,cores):
		threadz.append(st.threadWorker(ThreadProcess))
	qsender = (inQ,outQ,Benf,Timeo,veruficator)
	for thread in threadz:
		thread.run(qsender)
	print "Now loading data..."
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
	
	print "accumulating..."
	try:
		while True:
			outputlist.append(outQ.get(block=False))
			#print "blop"
	except Exception:
		pass
	print "starting thread kill"
	for thread in threadz:
		thread.end()
	
	
	#print outputlist
	outputlist.sort(key=itemgetter(0))
	print "writing"
	filename = args.file
	if Benf:
		filename += "_benf"
	else:
		filename += "_zipf"
	if Timeo:
		filename += "_time"
	else:
		filename += "_len"
	with open(filename + ".csv", "w") as outfile:
		for element in outputlist:
			outfile.write(str(element[0]) + ',' + str(element[1]) + '\n')
	print "it is now safe to shut down your computer"
