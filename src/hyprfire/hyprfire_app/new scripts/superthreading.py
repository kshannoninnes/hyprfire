import multiprocessing as satan


class ThreadWorker:
    def __init__(self, function):
        self.func = function

    def run(self, args):
        self.proc = satan.Process(target=self.func, args=args)
        self.proc.start()

    def end(self):
        self.proc.join()
