import tkinter as tk
import time
import csv
from numpy.random import randint

from manager import TimeManager
from  ..frames.baseframe import BaseFrame


class MentalCalcFrame(BaseFrame):
    def __init__(self, digit=2, master=None, path='./data/MentalCalc/', fname='mentalcalc.csv', q_max=None, timelimit=None):
        super().__init__(master)
        self.path = path
        self.fname = fname
        self.is_running = False
        
        self.question = self.create_question(digit) # [num1, num2]
        self.questions = [['num1', 'num2']]
        self.records = [['num1', 'num2', 'answer', 'result', 'time']]
        self.q_digit = digit
        self.q_cnt = 0
        self.q_max = q_max
        self.q_pos = 0
        self.q_value = tk.StringVar(value=str(self.question[0]))

        self.create_widgets()
        self.time_manager = TimeManager(self, tl=timelimit)
        if timelimit:
            self.time_manager.execute(self.exit_process, after=timelimit)

    def create_widgets(self):
        self.q_label = tk.Label(self, textvariable=self.q_value, relief=tk.RAISED, bg=self.bg)
        self.q_label['font'] = ('MSゴシック', 80, 'bold')
        #self.q_label.bind('<Button-1>', self.mouse_clicked)
        #self.q_label.bind('<Button-3>', self.mouse_clicked)
        #self.q_label.bind('<KeyPress>', self.key_pressed)
        self.q_label.bind('<KeyRelease>', self.key_pressed)
        self.q_label.focus_set()
        self.q_label.pack(expand=True, fill=tk.BOTH)

    def mouse_clicked(self, event):
        self.logger.debug("mouse clicked. %s", event)
        self.q_label.focus_set()
    
    def key_pressed(self, event):
        self.q_label.focus_set()
        key_name = event.keysym
        if 'KP_' in key_name:
            key_name = key_name.replace('KP_', '')
        var = self.q_value.get()
        POSNUM = 3
        if self.q_pos in [0, 1]:
            if key_name in ['Return', 'Enter']:
                self.q_pos = (self.q_pos + 1) % POSNUM
                self.change_label()
        else: # self.q_pos == 2
            if key_name in ['Return', 'Enter']:
                if not var == 0:
                    self.q_cnt += 1
                    self.submit_answer()
                    self.question = self.create_question(self.q_digit)
                    self.q_pos = (self.q_pos + 1) % POSNUM
                    self.change_label()
            elif key_name == 'BackSpace':
                if len(var) == 1:
                    self.q_value.set('0')
                else:
                    self.q_value.set(var[:-1])
            elif key_name.isdigit():
                if var == '0':
                    var = ''
                self.q_value.set(var + key_name)
            else:
                print(key_name)
    
    def change_label(self):
        if self.q_pos == 0:
            self.q_value.set(self.question[0])
        elif self.q_pos == 1:
            self.q_value.set(f'+{self.question[1]}')
        else:
            self.q_value.set('0')
    
    def submit_answer(self):
        num1, num2 = self.question
        ans = int(self.q_value.get())
        result = (num1 + num2 == ans)
        t = self.time_manager.elapsed_time
        ls = [num1, num2, ans, result, t]
        self.records.append(ls)
        self.logger.info('record: %s', ls)

    def save(self):
        with open(self.path + self.fname, 'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(self.records)
        self.logger.info('mentalcalc records is saved.: %s', self.fname)
    
    def exit_process(self):
        self.save()
        self.finish()

    @staticmethod
    def create_question(digit):
        '''
        繰り上がりの起きないdigit桁の整数の足し算を作成する．
        '''
        low = 10**(digit-1)
        high = 9*(10**(digit-1))
        num1 = randint(low=low, high=high)
        for i, v in enumerate(str(num1)):
            if i == 0:
                num2 = str(randint(low=1, high=10-int(v)))
            else:
                num2 += str(randint(low=0, high=10-int(v)))
        else:
            num2 = int(num2)
        return [num1, num2]


