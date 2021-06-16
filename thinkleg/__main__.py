import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from tasks.apps.taskapp import Tasks
from tasks.frames.tasksframe import TasksFrame
from arduino import Arduino
from mysocket.server import ThinkLegServer



class ThinkLegApp(Tasks):
    def __init__(self, datapath):
        
        self.logger = getLogger('thinkleg')
        self.datapath = datapath
        self.status = {'wait':-1, 'rest':0, 'mentalcalc':1, 'vas':2, 'stroop':3, 'calc':4}
        self.server = ThinkLegServer(host='localhost', port=12345)
        self.server.start()

        self.frame = None
        self.arduino = Arduino(self.datapath, 'arduino_data')
        self.arduino.start()

        super().__init__(datapath=datapath)
        self.create_widgets()
        self.logger.debug('ThinkLegApp is initialized.')

    def create_widgets(self):
        super().create_widgets()
        self.progress_frame = tk.Frame(self.first_frame)
        self.progress_label = tk.Label(self.progress_frame, text='Preparing for Arduino')
        self.progress_label.pack()
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(self.progress_frame,
            orient=tk.HORIZONTAL, variable=self.progress_var, maximum=60, length=200, mode='determinate'
        )
        self.progress_bar.pack()
        self.progress_frame.pack()
        if self.arduino:
            threading.Thread(target=self.__progress, daemon=True).start()
        self.logger.debug('widgets are created.')

    def __progress(self):
        st = time.time()
        latency = 60
        t = 0
        while t < latency:
            t = time.time()-st
            self.progress_var.set(t)
            time.sleep(2)
        self.progress_label['text'] = 'Arduino Ready.'
        self.progress_bar.destroy()

    def change_frame(self, to):
        self.logger.debug('change_frame is called.')
        if self.frame:
            self.logger.debug('%s is destroied.', self.frame)
            self.arduino.thinkleg_status = self.status['wait']
            self.frame.finish()
        
        if to == 'vas':
            self.arduino.thinkleg_status = self.status['vas']
            self.create_vasframe()
        elif to == 'calc':
            self.arduino.thinkleg_status = self.status['calc']
            self.create_calcframe()
        elif 'stroop' in to:
            self.arduino.thinkleg_status = self.status['stroop']
            self.create_stroopframe(int(to[-1]))
        elif 'mentalcalc' in to:
            self.arduino.thinkleg_status = self.status['mentalcalc']
            self.create_mentalcalc_frame(int(to[-1]))
    
    def finish(self):
        self.arduino.save('thinkleg')
        return super().finish()


class MainFrame(TasksFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        if self.master.arduino:
            threading.Thread(target=self.__progress, daemon=True).start()

    def create_widgets(self):
        self.progress_frame = tk.Frame(self)
        self.progress_label = tk.Label(self.progress_frame, text='Preparing for Arduino')
        self.progress_label.pack()
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(self.progress_frame,
            orient=tk.HORIZONTAL, variable=self.progress_var, maximum=60, length=200, mode='determinate'
        )
        self.progress_bar.pack()
        self.progress_frame.pack()

    def __progress(self):
        st = time.time()
        latency = 60
        t = 0
        while t < latency:
            t = time.time()-st
            self.progress_var.set(t)
            time.sleep(2)
        self.progress_label['text'] = 'Arduino Ready.'
        self.progress_bar.destroy()

    def change_frame(self, to):
        self.master.change_frame(to)





def main():
    datapath = f'./data/{datetime.now().strftime("%Y%m%d/%H-%M-%S")}/'
    os.makedirs(datapath, exist_ok=True)

    app = ThinkLegApp(datapath)
    app.mainloop()



if __name__ == '__main__':
    main()