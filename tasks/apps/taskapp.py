import os
import time
import threading
from datetime import datetime
import tkinter as tk
from json import load
from logging import config, getLogger
from typing import Collection
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from .baseapp import BaseApp
from ..frames import TasksFrame
from ..frames import VasFrame
from ..frames import CalcFrame
from ..frames import StroopFrame
from ..frames import MentalCalcFrame
from ..frames import TappingFrame
from mysocket.server import ThinkLegServer



class TasksApp(BaseApp):
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
        self.first_frame = TasksFrame(self)
        self.first_frame.grid(row=0, column=0, sticky="nsew")        
        self.logger.debug('widgets are created.')

    def create_vas_frame(self):
        self.frame = VasFrame(self, path=self.datapath, fname='vas.csv')
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.logger.info('vas frame is created.')

    def create_calc_frame(self):
        self.frame = CalcFrame(self, path=self.datapath, fname='calc.csv')
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.logger.info('calc frame is created.')

    def create_tapping_frame(self, num):
        self.frame = TappingFrame(num, self, path=self.datapath, fname='tapping.csv', timelimit=30)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.logger.info('tapping%s, frame is created', num)

    def create_mentalcalc_frame(self, num):
        self.frame = MentalCalcFrame(num, master=self, path=self.datapath, fname=f'mentalcalc{num}.csv')
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.logger.info('mentalcalc%s, frame is created.', num)

    def create_stroop_frame(self, task):
        self.frame = StroopFrame(task, master=self, path=self.datapath, fname=f'stroop{task}.csv')
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.logger.info('stroop%s frame is created.', task)

    def change_frame(self, to):
        self.logger.debug('change_frame is called.')
        if self.frame:
            self.logger.debug('%s is destroied.', self.frame)
            self.frame.finish()
        if to == 'vas':
            self.create_vas_frame()
        elif to == 'calc':
            self.create_calc_frame()
        elif 'stroop' in to:
            self.create_stroop_frame(int(to[-1]))
        elif 'mentalcalc' in to:
            self.create_mentalcalc_frame(int(to[-1]))
        elif 'tapping' in to:
            self.create_tapping_frame(int(to[-1]))
    
    def finish(self):
        return super().finish()








