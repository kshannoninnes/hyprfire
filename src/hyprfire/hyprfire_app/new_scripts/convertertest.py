from hyprfire_app.new_scripts import pcapconverter, dumpfile, packetdata
import os, multiprocessing, time

def convertertest():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    testpath = os.path.join(dirpath, "bigtest.pcap")
    startTime = time.time()
    file = pcapconverter.pcapConverter(testpath)
    print(f"Standalone took {time.time() - startTime} seconds")
    print(f"First packet: {file[0].epochTimestamp}")
    print(f"Wireshark says: 1583450622.725460000")
    print(f"Last packet: {file[-1].epochTimestamp}")
    print("Wireshark says: 1583450662.832554000")
def call(filename, i):
    startTime = time.time()
    print(f"Starting process {i}")
    file = pcapconverter.pcapConverter(filename)
    #print(f"Process {i} output: name = {file.filename} packet list = {len(file.packets)}")
    print(f"Process {i} took {time.time() - startTime} seconds")

class ThreadWorker:
    def __init__(self, function):
        self.func = function

    def run(self, args):
        self.proc = multiprocessing.Process(target=self.func, args=args)
        self.proc.start()

    def end(self):
        self.proc.join()

if __name__ == '__main__':
    convertertest()