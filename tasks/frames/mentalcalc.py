import tkinter as tk
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from  ..frames.baseframe import BaseFrame


class MentalCalcFrame(BaseFrame):
    def __init__(self, digit, master=None, path='./data/MentalCalc/', fname='mentalcalc.csv'):
        super().__init__(master)
        self.logget = None
        self.path = path
        self.fname = fname
        self.q_cnt = 0
        self.q_num_max = 10000
        self.questions = [['num_l1', '+or-', 'num_l2', '=', 'val', 'correct']]
        self.answers = [['answer', 'result', 'time']]

        self.create_widgets()

    def create_widgets(self):
        self.q_label = tk.Label(self, text='Ready?', relief=tk.RAISED, bg=self.bg)
        self.q_label['font'] = ('MSゴシック', 80, 'bold')
        self.q_label.bind('<Button-1>', self.mouse_clicked)
        self.q_label.bind('<Button-3>', self.mouse_clicked)
        self.q_label.pack(expand=True, fill=tk.BOTH)

    def mouse_clicked(self, event):
        self.logger.debug("mouse clicked. %s", event)
