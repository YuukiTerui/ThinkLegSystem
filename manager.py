import time


class TimeManager():
    def __init__(self, master, tl=None):
        self.master = master
        self.start_time = time.time()
        self.time_limit = tl

    @property
    def elapsed_time(self):
        return time.time() - self.start_time()

    @property
    def is_timeover(self):
        if self.time_limit == None:
            return False
        t = time.time()
        if t - self.start_time < self.time_limit:
            return False
        return True

    