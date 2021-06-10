import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import Label, ttk
from json import load
from logging import config, getLogger
from tkinter.constants import HORIZONTAL
from typing import SupportsRound
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from .baseapp import BaseApp, BaseFrame
from .vas import VasFrame
from .calc import CalcFrame
from server import ThinkLegServer



class Tasks(BaseApp):
    def __init__(self, datapath):
        super().__init__()
        self.title('ThinkLegTaskApp')
        self.logger = getLogger('thinkleg')
        self.datapath = datapath
        self.states = {'wait':0, 'task':1, 'rest':2, 'vas':3, 'stroop':4}
        self.server = ThinkLegServer(host='localhost', port=12345)
        self.server.start()

        self.frame = None

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
        self.logger.debug('change_frame is called.')
        if self.frame:
            self.logger.debug('%s is destroied.', self.frame)
            self.frame.finish()
        if to == 'vas':
            self.create_vas()
        elif to == 'calc':
            self.create_calc()
    
    def finish(self):
        return super().finish()


class MainFrame(BaseFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text='Think Leg System')
        self.title_label.pack()

        self.vas_button = tk.Button(self, text='vas', command=lambda:self.change_frame('vas'))
        self.vas_button.pack()

        self.calc_button = tk.Button(self, text='calc', command=lambda:self.change_frame('calc'))
        self.calc_button.pack()

        self.finish_button = tk.Button(self, text='finish', command=lambda: self.master.finish())
        self.finish_button.pack()

    def change_frame(self, to):
        self.master.change_frame(to)





def main():
    datapath = f'./data/{datetime.now().strftime("%Y%m%d/%H-%M-%S")}/'
    os.makedirs(datapath, exist_ok=True)

    app = Tasks(datapath)
    app.mainloop()



if __name__ == '__main__':
    main()