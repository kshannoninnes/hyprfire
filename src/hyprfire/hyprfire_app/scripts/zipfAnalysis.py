import math
#=================================================================================
#GetSortedZipfCats
#Creates a list of buckets of categorised lengths sorted from most to least common
def GenSortedZipfCats(valuesNShit):
	bucketeer = {}
	finallist = []
	for value in valuesNShit:
		scwa = bucketeer.get(value[1],[]) #we use one cause of what is in Omnifilter and in Primarch
		scwa.append(value)
	#	print scwa
		bucketeer[value[1]] = scwa
	keys = bucketeer.keys()
	keys.sort()
	keys.reverse()
	for key in keys:
		for element in bucketeer[key]:
			finallist.append(element)
	#print bucketeer
	return finallist
#=================================================================================
#GetZipfCats
#Creates a list of buckets of categorised lengths
def GenZipfCats(valuesNShit):
	bucketeer = {}
	for value in valuesNShit:
		scwa = bucketeer.get(value[1],[]) #we use one cause of what is in Omnifilter and in Primarch
		scwa.append(value)
	#	print scwa

		bucketeer[value[1]] = scwa
	#print bucketeer
	scree = bucketeer.values()
	return scree
#=================================================================================
#GetZipfBuckets
#Takes in a list of numbers, returns the top ten buckets
def GetZipfBuckets(valuesNShit):
	bucketeer = {}
	for value in valuesNShit:
		bucketeer[value] = bucketeer.get(value,0) + 1
	superTopList = []
	resultList = list(bucketeer.values())
	while len(resultList) < 10:
		resultList.append(0)
	resultList.sort()
	resultList.reverse()
	#print resultList
	for i in range(0,10):
		superTopList.append( float(resultList[i])/float(len(valuesNShit)))
	return superTopList
#=================================================================================
#GetZipfBuckets
#Takes in a list of numbers, returns the top ten buckets
def GetZipfBucketTotals(valuesNShit):
	bucketeer = {}
	for value in valuesNShit:
		bucketeer[value] = bucketeer.get(value,0) + 1
	superTopList = []
	resultList = bucketeer.values()
	while len(resultList) < 10:
		resultList.append(0)
	resultList.sort()
	resultList.reverse()
	#print resultList
	return resultList
#=================================================================================
#def GetMostPopularCategory(valuesNShit):
#	bucketeero = {}
#	for value in valuesNShit:
#		vv = bucketeero.get(value,0)
#		bucketeero[value] = vv + 1
#	keyArr = sorted(bucketeero.iteritems(), key=lambda(k,v): (v,k))
#	return keyArr[0][0]
#=================================================================================
#GenZipfSeries
#Takes in a number, returns the supposed top ten
def GenZipfSeries(numero):
	listero = []
	listero.append(numero)
	for i in range(1,10):
		listero.append(numero/i)
	return listero
#=================================================================================
#GetZipfU
#Does the Watson variant of the Cramer von Mises test against the Zipf Series.
def GetZipfU(probabilityList):
	n = 10
	subTotal = 0
	zedBar = GetWatsonZedBar(probabilityList)
	for i in range (0,n):
		subTotal += math.pow((GetWatsonZed(i,probabilityList) - zedBar),2) * GetWatsonWeight(i,probabilityList)
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
def GetWatsonZed(listIndex,list):
	benfList = GenZipfSeries(list[0])
	Si = AccumulateTo(list,listIndex)
	Ti = AccumulateTo(benfList, listIndex)
	zed = Si - Ti
	return zed
#=================================================================================
#GetWatsonZedBar
#gets the Z-bar value for a benfords list and a list of probs
def GetWatsonZedBar(list):
	totalElements = 10
	zedBar = 0
	for i in range(0,totalElements):
		partBar = GetWatsonWeight(i,list) * GetWatsonZed(i,list)
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
