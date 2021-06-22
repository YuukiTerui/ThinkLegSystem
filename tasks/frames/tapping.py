from manager import TimeManager
import tkinter as tk
import time
from numpy.random import randint
from json import load
from logging import config, getLogger
from os import path
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from .baseframe import BaseFrame
from ...manager import TimeManager


class TappingFrame(BaseFrame):
    def __init__(self, digit=2, master=None, path='./data/tapping/', fname='tapping.csv', timelimit=None):
        super().__init__(master)
        self.logger = getLogger('gui.frame')
        self.path = path
        self.fname = fname
        self.is_running = False
        self.cnt = 0
        self.digit = digit
        self.question = [] # [num, ans, time]
        self.records = []

        self.create_widgets()
        self.time_manager = TimeManager(self, tl=timelimit)
        
    def create_widgets(self):
        self.num = tk.StringVar(value=self.create_question(self.digit))
        self.label_pos = 0
        self.num_label = tk.Label(self, textvariable=self.num, relief=tk.RAISED, bg=self.bg)
        self.num_label['font'] = ('MSゴシック', 80, 'bold')
        self.num_label.bind('<KeyRelease>', self.key_pressed)
        self.num_label.focus_set()
        self.num_label.pack(expand=True, fill=tk.BOTH)
        return super().create_widgets()

    def key_pressed(self, event):
        key_name = event.keysym
        if 'KP_' in key_name:
            key_name = key_name.replace('KP_', '')
        var = self.num.get()
        POSNUM = 2
        if self.label_pos == 0:
            if key_name in ['Return', 'Enter']:
                self.num.set('0')
                self.label_pos = (self.label_pos + 1) % POSNUM
                self.change_label()
        else: # label_pos = 1
            if key_name in ['Return', 'Enter']:
                if not var == 0:
                    self.cnt += 1
                    self.submit_answer()
                    self.label_pos = (self.label_pos + 1) % POSNUM
                    self.question = self.create_question(self.digit)
                    self.change_label()
            elif key_name == 'BackSpace':
                if len(var) == 1:
                    self.num.set('0')
                else:
                    self.num.set(var[:-1])
            elif key_name.isdigit():
                if var == '0':
                    var = ''
                self.num.set(var + key_name)
            else:
                print(key_name)
    
    def submit_answer(self):
        ans = int(self.num.get())
        t = self.time_manager.elapsed_time
        ls = [ans, t]
        self.records.append(ls)
        self.logger.info('record: %s', ls)

    def change_label(self):
        if self.label_pos == 0:
            self.num.set(str(self.question))
        else:
            self.num.set('0')

    @staticmethod
    def create_question(digit):
        return randint(low=10**(digit-1), high=9*(10**(digit-1)))
