import bz2

class FileReader:
	def __init__(self,fileName,windowSize):
		fileArr = fileName.split('.')
		filetype = fileArr[-1]
		self.file = open(fileName, "r")
		if filetype == 'bz2':
			self.file.close()
			self.file = bz2.BZ2File(fileName)		
		self.winSize = int(windowSize)

	def Get(self):
		linestruct = []
		counter = 0
		for line in self.file:
			try:
				lin = line.split(',')
				linestruct.append(lin)
				counter += 1
				if counter == self.winSize:
					yield linestruct
					linestruct = []
					counter = 0
			except Exception:
				print("This is filereader skipping invalid line " + line)
				
	def RawGet(self):
		linestruct = []
		counter = 0
		for line in self.file:
			linestruct.append(line)
			counter += 1
			if counter == self.winSize:
				yield linestruct
				linestruct = []
				counter = 0



def GetN2DTime(elem):
	arr = elem.split(',')
	return int(arr[0])


