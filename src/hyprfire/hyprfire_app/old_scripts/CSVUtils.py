import os
import bz2

def MergeCSVFiles(ListOfFiles, outFile, sortColumn, bzMode):
	with bz2.BZ2File(outFile + '.bz2',"w") if bzMode else open(outFile,"w") as outFP:
		fileConstruct = []
		for filename in ListOfFiles:
			if bzMode:
				temp = bz2.BZ2File(filename,"r")
			else:
				temp = open(filename,"r")
			tt = [temp,None]
			fileConstruct.append(tt)
		while True:
			fileConstruct = GetFreshLines(fileConstruct)
			ShouldIStopNow = True
			minnum = 0
			elemID = 0
			counter = 0
			for pair in fileConstruct:
				if pair[1] != "":
					ShouldIStopNow = False
					splitsies = pair[1].split(',')
					factor = int(splitsies[sortColumn])
					if factor < minnum or minnum == 0:
						minnum = factor
						elemID = counter
				counter += 1
			if ShouldIStopNow:
				break
			else:
				outFP.write(fileConstruct[elemID][1])
				fileConstruct[elemID][1] = None
		for elem in fileConstruct:
			elem[0].close()
		for filename in ListOfFiles:
			os.remove(filename)

def GetFreshLines(fileconst):
	for elem in fileconst:
		if elem[1] is None:
			elem[1] = elem[0].readline()
	return fileconst

def IsBZMode(filename):
	filetype = filename.split('.')[-1]
	if filetype == 'bz2':
		print("BZ2 file detected, activating BZMode!")
		return True
	else:
		return False
