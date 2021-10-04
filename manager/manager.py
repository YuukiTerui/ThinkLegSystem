import time
from datetime import datetime
from threading import Thread, Event


class TimeManager():
    def __init__(self, master, tl=None):
        self.master = master
        self.start_time = time.time()
        self.time_limit = tl

    @property
    def elapsed_time(self):
        return time.time() - self.start_time

    @property
    def datetime(self):
        return datetime.now()

    @property
    def is_timeover(self):
        if self.time_limit == None:
            return False
        t = time.time()
        if t - self.start_time < self.time_limit:
            return False
        return True

    def execute(self, func, after=0):
        if not isinstance(after, int):
            raise TypeError
        event = Event()
        def th_func():
            event.wait(timeout=after)
            func()
        thread  = Thread(target=th_func, daemon=True)
        thread.start()