import math
import re
import bz2
#=================================================================================
#GetRstArrivalTimes
#Takes in a file, returns a list of all the FIN packet arrival times
def GetRstArrivalTimes(fileName):
	regex = re.compile('.*\[R\].*')
	microsecondlist = []
	newFile = bz2.BZ2File(fileName)

	for line in newFile:
		if not(regex.match(line) is None):
			contents = line.split(' ')
			time = contents[0]
			timecontents = time.split(':')

			hours = int(timecontents[0])
			minutes = int(timecontents[1]) + (hours*60)
			seconds = float(timecontents[2]) + float(minutes * 60)
			microseconds = int(seconds * 1000000) #the difference could be veeery small

			if microseconds != 0:
				microsecondlist.append(microseconds)

	newFile.close()
	#print "DEBUG: LIST IS "
	#print microsecondlist

	return microsecondlist
#=================================================================================
#GetFinArrivalTimes
#Takes in a file, returns a list of all the FIN packet arrival times
def GetFinArrivalTimes(fileName):
	regex = re.compile('.*\[F\].*')
	microsecondlist = []
	newFile = bz2.BZ2File(fileName)

	for line in newFile:
		if not(regex.match(line) is None):
			contents = line.split(' ')
			time = contents[0]
			timecontents = time.split(':')

			hours = int(timecontents[0])
			minutes = int(timecontents[1]) + (hours*60)
			seconds = float(timecontents[2]) + float(minutes * 60)
			microseconds = int(seconds * 1000000) #the difference could be veeery small

			if microseconds != 0:
				microsecondlist.append(microseconds)

	newFile.close()
	#print "DEBUG: LIST IS "
	#print microsecondlist

	return microsecondlist
#=================================================================================
#GetSynArrivalTimes
#Takes in a file, returns a list of all the SYN packet arrival times
def GetSynArrivalTimes(fileName):
	regex = re.compile('.*\[S\].*')
	microsecondlist = []
	newFile = bz2.BZ2File(fileName)

	for line in newFile:
		if not(regex.match(line) is None):
			contents = line.split(' ')
			time = contents[0]
			timecontents = time.split(':')

			hours = int(timecontents[0])
			minutes = int(timecontents[1]) + (hours*60)
			seconds = float(timecontents[2]) + float(minutes * 60)
			microseconds = int(seconds * 1000000) #the difference could be veeery small

			if microseconds != 0:
				microsecondlist.append(microseconds)

	newFile.close()
	#print "DEBUG: LIST IS "
	#print microsecondlist

	return microsecondlist
#===============================================================================
#GetUDPArrivalTimes
#Takes in a file, returns a list of all the UDP packet arrival times
def GetUDPArrivalTimes(fileName):
	regex = re.compile('.*UDP.*')
	microsecondlist = []
	newFile = bz2.BZ2File(fileName)

	for line in newFile:
		if not(regex.match(line) is None):
			contents = line.split(' ')
			time = contents[0]
			timecontents = time.split(':')

			hours = int(timecontents[0])
			minutes = int(timecontents[1]) + (hours*60)
			seconds = float(timecontents[2]) + float(minutes * 60)
			microseconds = int(seconds * 1000000) #the difference could be veeery small

			if microseconds != 0:
				microsecondlist.append(microseconds)

	newFile.close()
	#print "DEBUG: LIST IS "
	#print microsecondlist

	return microsecondlist
#===============================================================================
#GetTCPArrivalTimes
#Takes in a file, returns a list of all the TCP packet arrival times
def GetTCPArrivalTimes(fileName):
	regex = re.compile('.*Flags.*')
	regexTwo = re.compile('.* IP .*')
	regexThree = re.compile('.* IP6 .*')
	microsecondlist = []
	newFile = bz2.BZ2File(fileName)

	for line in newFile:
		if not(regex.match(line) is None) and (not(regexTwo.match(line) is None) or not(regexThree.match(line) is None)):
			microseconds = 0
			try:
				contents = line.split(' ')
				time = contents[0]
				timecontents = time.split(':')

				hours = int(timecontents[0])
				minutes = int(timecontents[1]) + (hours*60)
				seconds = float(timecontents[2]) + float(minutes * 60)
				microseconds = int(seconds * 1000000) #the difference could be veeery small
			except ValueError:
				print( "Error in value access: " + line)
			if microseconds != 0:
				microsecondlist.append(microseconds)

	newFile.close()
	#print "DEBUG: LIST IS "
	#print microsecondlist

	return microsecondlist
#===============================================================================
#GetLengthPairs
#takes in a file, and then reads in times and lengths.
def GetLengthPairs(fileName):
	ipRegex = re.compile('.* IP .*|.* IP6 .*')
	timeRegex = re.compile('.*([0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9]*).*')
	lenRegex = re.compile('.*length ([0-9]*).*')
	bzFile = bz2.BZ2File(fileName)
	lengthPairList = {}

	for line in bzFile:
		if not (ipRegex.match(line) is None):
			timeCollector = timeRegex.match(line)
			lenCollector = lenRegex.match(line)
			microseconds = 0
			if not (timeCollector is None) and not (lenCollector is None):
				try:
					time = timeCollector.group(1)
					timecontents = time.split(':')

					hours = int(timecontents[0])
					minutes = int(timecontents[1]) + (hours*60)
					seconds = float(timecontents[2]) + float(minutes * 60)
					microseconds = int(seconds * 1000000)
				except ValueError:
					print("Error in value access: " + line)
				if microseconds != 0:
					lengthPairList[microseconds] = int(lenCollector.group(1))
	bzFile.close()
	return lengthPairList
#===============================================================================
#GetBuckets
#Takes in a *SORTED* list of arrival times, and a window size, and then returns the list of times as a list of windows.
def GetBuckets(microsecondlist,windowSize):
	#firstly, check to see if the window size was defined properly
	windowList = []
	formatVariable = windowSize[-1:]
	timeValue = int(windowSize[:-1])
	if formatVariable not in ['s','m','h','d']:
		print("ERROR: window specifier of " + formatVariable + " is invalid")
		windowList.append(microsecondlist)
	else:
		if timeValue <= 0:
			print("ERROR: Invalid window size of " + str(timeValue))
			windowList.append(microsecondlist)
		else:
			#Okay, so we're valid. Lets do some maths! :D	
			#we need to determine the window size in microseconds.
			windowline = {
				's': lambda secs: secs * 1000000,
				'm': lambda mins: mins * 60 * 1000000,
				'h': lambda hors: hors * 60 * 60 * 1000000,
				'd': lambda days: days * 24 * 60 * 60 * 1000000,
			}[formatVariable](timeValue)
			#easy peasy right? <3 lambda :P
			#now, we need to construct the windows. We can do this the fast way, or the slow way. I vote the fast way.
			windowLimit = microsecondlist[0] + windowline
			newarr = []
			for thingo in microsecondlist:
				if thingo > windowLimit:
					windowList.append(newarr)
					windowLimit += windowline
					newarr = []
				newarr.append(thingo)
			windowList.append(newarr)
	return windowList
#===============================================================================
#GetBucketsByPacket
#Takes a list and a number of packets and sorts them into windowed lists
def GetBucketsByPacket(elementList,windowSize):
	windowList = []
	if windowSize <= 0:
		print("Error: Invalid Window size of " + str(windowSize))
		windowList.append(elementList)
	else:
		i = 0
		newWin = []
		for element in elementList:
			if i > windowSize:
				windowList.append(newWin)
				newWin = []
				i = 0
			i += 1
			newWin.append(element)
	return windowList
#===============================================================================
#DictionaryRebucket
#Takes a list of buckets, and a dictionary, and transposes the dictionary components to buckets.
def DictionaryRebucket(bucketList,magicDict):
	retBuckets = []
	newBucket = []

	for bucket in bucketList:
		newBucket = []
		for value in bucket:
			newBucket.append(magicDict[value])
		retBuckets.append(newBucket)
	return retBuckets
#===============================================================================
#ImportPrimes
#For a given filename, take in the primes and return as list
def ImportPrimes(fileName):
	listOfPrimes = []
	thefile = open(fileName)
	for line in thefile:
		listOfPrimes.append(int(line))
	return listOfPrimes
#===============================================================================
#GetInterArrivalTimes
#Takes a list of arrival times, finds out what the interarrival times are.
def GetInterArrivalTimes(microsecondlist):
	currentTime = 0
	timeDiffList = []
	try:
		currentTime = microsecondlist[0]
	except Exception:
		currentTime = microsecondlist.next()

	for time in microsecondlist:
		timeDiffList.append(time - currentTime)
		currentTime = time

	return timeDiffList
#================================================================================
#GetBenfordsBuckets
#Takes a list of numbers, and a digit index, spits out the benford's prob of the indexth digit
def GetBenfordsBuckets(numberList, index):
	realIndex = index - 1
	bucketList = [0,0,0,0,0,0,0,0,0,0]
	probabilityList = [0,0,0,0,0,0,0,0,0,0]
	totalNumOfValidEntries = 0
	for time in numberList:
		if time > 0:
			stringied = str(time)
			#print stringied
			try:
				firstElement = int(stringied[realIndex])
			except IndexError:
				#print "ERROR, No such value for index " + str(realIndex) + " and time " + stringied
				firstElement = 0
			bucketList[firstElement] += 1
			totalNumOfValidEntries +=1

	if totalNumOfValidEntries != 0:
		for i in range(0,10):
			probabilityList[i] = float(bucketList[i]) / totalNumOfValidEntries
	return probabilityList
#================================================================================
#GetFirstDigit
#Gives you the first digit
def GetFirstDigit(number,index):
	digit = 0
	realIndex = index - 1
	if number > 0:
		stringied = str(number)
		try:
			firstElement = int(stringied[realIndex])
		except IndexError:
			firstElement = 0
		digit = firstElement
	return digit
#================================================================================
#GetBenfordsBucketTotals
#Does not perform the probability refinement
def GetBenfordsBucketTotals(numberList, index=1):
	realIndex = index - 1
	bucketList = [0,0,0,0,0,0,0,0,0,0]
	#probabilityList = [0,0,0,0,0,0,0,0,0,0]
	totalNumOfValidEntries = 0
	for time in numberList:
		if time > 0:
			stringied = str(time)
			#print stringied
			try:
				firstElement = int(stringied[realIndex])
			except IndexError:
				#print "ERROR, No such value for index " + str(realIndex) + " and time " + stringied
				firstElement = 0
			bucketList[firstElement] += 1
			totalNumOfValidEntries +=1

	return bucketList
#================================================================================
#GetTotalNumberOfBucketedElements
#Adds all the bucket values together, tells you how many things are in there
def GetTotalNumberOfBucketedElements(bucketList):
	totalNum = 0
	for bucket in bucketList:
		totalNum += bucket
	return totalNum
#================================================================================
#GetExpectedNumberUnderBenfords
#Gets the expected frequency under the benfords of index
def GetExpectedNumberUnderBenfords(totalNumberOfElements,index):
	benf = GetBenfordSeries(index)
	fuzzy = []
	for element in benf:
		fuzzy.append(element * totalNumberOfElements)
	return fuzzy
#================================================================================
#GetBenfordSeries
#Takes an index, returns the relevant Benfords Series
def GetBenfordSeries(index):
	if index == 1:
		return [0.000,0.301,0.176,0.125,0.097,0.079,0.067,0.058,0.051,0.046]
	elif index == 2:
		return [0.120,0.114,0.109,0.104,0.100,0.097,0.093,0.090,0.088,0.085]
	elif index == 3:
		return [0.102,0.101,0.101,0.101,0.100,0.100,0.099,0.099,0.099,0.098]
	else:
		return [0.100,0.100,0.100,0.100,0.100,0.100,0.100,0.100,0.100,0.100]
#================================================================================
#GetBetterBenfordSeries
#Takes an index, returns the relevant Benfords Series
def GetBetterBenfordSeries(index):
	if index == 1:
		return [0.301,0.176,0.125,0.097,0.079,0.067,0.058,0.051,0.046]
	elif index == 2:
		return [0.120,0.114,0.109,0.104,0.100,0.097,0.093,0.090,0.088,0.085]
	elif index == 3:
		return [0.102,0.101,0.101,0.101,0.100,0.100,0.099,0.099,0.099,0.098]
	else:
		return [0.100,0.100,0.100,0.100,0.100,0.100,0.100,0.100,0.100,0.100]

#================================================================================
#GetBenfordSSE
#Takes in a Benfords Bucket list, an index, and then compares with the Benfords Series
def GetBenfordSSE(probList, index):
	benfordList = GetBenfordSeries(index)
	sume = 0
	for i in range(0,10):
		if probList[i] != 0:
			sume += math.pow((probList[i]-benfordList[i]),2)
	return sume
#=================================================================================
#GetBenfordPCS
#Does the Pearsons Chi Squared test between the given data and the Benfords Series
def GetBenfordPCS(bucketList, index):
	benfordList = GetBenfordSeries(index)
	sume = 0
	for i in range(0,10):
		if bucketList[i] != 0:
			tempVal = bucketList[i] - benfordList[i]
			tempVal = math.pow(tempVal,2)
			tempVal = tempVal/benfordList[i]
			if index == 1:
				tempVal = tempVal * 9
			else:
				tempVal = tempVal * 10
			sume += tempVal
	return sume
#=================================================================================
#GetBenfordsU
#Does the Watson variant of the Cramer von Mises test against the Benfords Series.
def GetBenfordU(probabilityList,benfordsIndex):
	n = 10
	if benfordsIndex == 1:
		n = 9
		probabilityList = probabilityList[1:]
	subTotal = 0
	zedBar = GetWatsonZedBar(benfordsIndex,probabilityList)
	for i in range (0,n):
		subTotal += math.pow((GetWatsonZed(benfordsIndex,i,probabilityList) - zedBar),2) * GetWatsonWeight(i,probabilityList)
	total = subTotal * n
	return total
#=================================================================================
#AccumulateTo
#Accumulates to an index of the list
def AccumulateTo(list,index):
	sumz = 0
	for i in range(0,index):
		sumz += list[i]
	return sumz
#=================================================================================
#GetWatsonZed
#gets the Z value for a certain index and benfords index
def GetWatsonZed(benfordsIndex,listIndex,list):
	benfList = GetBetterBenfordSeries(benfordsIndex)
	Si = AccumulateTo(list,listIndex)
	Ti = AccumulateTo(benfList, listIndex)
	zed = Si - Ti
	return zed
#=================================================================================
#GetWatsonZedBar
#gets the Z-bar value for a benfords list and a list of probs
def GetWatsonZedBar(benfordsIndex,list):
	totalElements = 10
	if benfordsIndex == 1:
		totalElements = 9
	zedBar = 0
	for i in range(0,totalElements):
		partBar = GetWatsonWeight(i,list) * GetWatsonZed(benfordsIndex,i,list)
		zedBar += partBar
	return zedBar
#=================================================================================
#GetWatsonWeight
#gets the t value (weight) for any given list index and benford index
def GetWatsonWeight(listIndex,list):
	weight = 0

	if listIndex == (len(list)-1):
		weight = list[listIndex] + list[0]
		weight = weight / 2
	else:
		weight = list[listIndex] + list[listIndex+1]
		weight = weight / 2
	return weight
#=================================================================================
#GetBenfordsAnalysisThreshold
#Returns the analysis threshold depending on the type required.
def GetBenfordsAnalysisThreshold(benftype):
	if benftype == 'U':
		return 0.205
	elif benftype == 'P':
		return 15.507
	elif benftype == 'S':
		return 0.1
	else:
		return 0
#=================================================================================
#GetBenfordsAnalysis
#Returns the analysis depending on the type required.
def GetBenfordsAnalysis(probabilityList, index, benftype):
	if benftype == 'U':
		return GetBenfordU(probabilityList,index)
	elif benftype == 'P':
		return GetBenfordPCS(probabilityList,index)
	elif benftype == 'S':
		return GetBenfordSSE(probabilityList,index)
	else:
		return 0
