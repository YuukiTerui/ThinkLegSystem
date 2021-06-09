import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from json import load
from logging import config, getLogger
from tkinter.constants import HORIZONTAL
from typing import SupportsRound
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from tasks.baseapp import BaseApp, BaseFrame
from tasks.vas import VasFrame
from tasks.calc import CalcFrame
from arduino import Arduino
from server import ThinkLegServer



class ThinkLegApp(BaseApp):
    def __init__(self, datapath):
        super().__init__()
        self.logger = getLogger('thinkleg')
        self.datapath = datapath
        self.state = 0
        self.server = ThinkLegServer(host='localhost', port=12345)
        self.thread_server = threading.Thread(target=self.server.run, daemon=True)
        self.thread_server.start()

        self.frame = None
        self.arduino = Arduino(self.datapath, 'arduino_data.csv')

        self.create_widgets()
        self.logger.debug('ThinkLegApp is initialized.')

    def create_widgets(self):
        self.first_frame = MainFrame(self)
        self.first_frame.grid(row=0, column=0, sticky="nsew")        
        self.logger.debug('widgets are created.')

    def create_vas(self):
        self.frame = VasFrame(self, path=self.datapath, fname='vas.csv')
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.logger.info('vas frame is created.')

    def create_calc(self):
        self.frame = CalcFrame(self, path=self.datapath, fname='calc.csv')
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.logger.info('calc frame is created.')

    def change_frame(self, to):
        #self.first_frame.pack_forget()
        self.logger.debug('change_frame is called.')
        if self.frame:
            self.logger.debug('%s is destroied.', self.frame)
            self.frame.destroy()
        if to == 'vas':
            self.create_vas()
        elif to == 'calc':
            self.create_calc()


class MainFrame(BaseFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        if self.master.arduino:
            threading.Thread(target=self.__progress).start()

    def create_widgets(self):
        self.title_label = tk.Label(self, text='Think Leg System')
        self.title_label.pack()

        self.vas_button = tk.Button(self, text='vas', command=lambda:self.change_frame('vas'))
        self.vas_button.pack()

        self.calc_button = tk.Button(self, text='calc', command=lambda:self.change_frame('calc'))
        self.calc_button.pack()

        self.progress_frame = tk.Frame(self)
        self.progress_label = tk.Label(self.progress_frame, text='Preparing for Arduino')
        self.progress_label.pack()
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(self.progress_frame,
            orient=HORIZONTAL, variable=self.progress_var, maximum=60, length=200, mode='determinate'
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
        self.progress_label['text'] = 'Arduino Ready.'
        self.progress_bar.destroy()


    def change_frame(self, to):
        #self.first_frame.pack_forget()
        self.logger.debug('change_frame is called.')
        if self.frame:
            self.logger.debug('%s is destroied.', self.frame)
            self.frame.destroy()
        if to == 'vas':
            self.create_vas()
        elif to == 'calc':
            self.create_calc()



def main():
    datapath = f'./data/{datetime.now().strftime("%Y%m%d/%H-%M-%S")}/'
    os.makedirs(datapath, exist_ok=True)

    app = ThinkLegApp(datapath)
    app.mainloop()



if __name__ == '__main__':
    main()