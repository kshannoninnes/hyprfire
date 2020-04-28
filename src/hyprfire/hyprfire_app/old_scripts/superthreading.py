import multiprocessing as satan

class threadWorker:
	def __init__(self,function):
		self.func = function
	def run(self,args):
		self.proc = satan.Process(target=self.func, args=(args))
		self.proc.start()
	def end(self):
		self.proc.join()

class semaphore:
	def __init__(self):
		self.val = satan.Value('i',0)
	def flip(self):
		if self.val.value == 0:
			self.val.value = 1
		else:
			self.val.value = 0
	def check(self):
		if self.val.value == 1:
			return True
		else:
			return False

def GetCores():
	return satan.cpu_count()

def GetQueue():
	return satan.Queue()