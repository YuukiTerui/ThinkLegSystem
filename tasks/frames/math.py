# coding: utf-8
import csv
import time
import tkinter as tk
from threading import Thread, Event
import numpy as np
from random import random, randint, sample
from datetime import datetime

from .baseframe import BaseFrame


class MATHFrame(BaseFrame):
    def __init__(self, master=None, fname=None, path='./'):
        super().__init__(master)
        self.path = path
        self.fname = fname

        self.labelstate = None
        self.clicked = False
        self.level = 3
        self.q = None
        self.judgement = None
        self.records = [] # [level num1 +/- num2 ans result]

        self.set_bind(self)
        self.font = ('', 50, 'bold')
        self.create_widgets()

        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()
        self.thread_event = Event()

        
    def set_bind(self, obj):
        obj.bind('<Button-1>', self.mouse_clicked)
        obj.bind('<Button-3>', self.mouse_clicked)
        
    def mouse_clicked(self, event):
        if not self.clicked:
            self.clicked = True
            self.thread_event.set()
            if event.num == 1:
                self.judge(self.q, True)
            elif event.num == 3:
                self.judge(self.q, False)
    
    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.qframe = self.create_qframe()
        self.qframe.grid(row=0, column=0, sticky='nsew')
        self.eqframe = self.create_eqframe()
        self.eqframe.grid(row=0, column=0, sticky='nsew')
        self.ansframe = self.create_ansframe()
        self.ansframe.grid(row=0, column=0, sticky='nsew')
        self.intframe = self.create_intframe()
        self.intframe.grid(row=0, column=0, sticky='nsew')
        
    def create_qframe(self):
        frame = tk.Frame(self)
        self.qtxt = tk.StringVar(value='question')
        qlabel = tk.Label(frame, textvariable=self.qtxt, font=self.font)
        qlabel.pack(anchor='center',expand=True)
        return frame
        
    def create_eqframe(self):
        frame = tk.Frame(self)
        label = tk.Label(frame, text='EQUAL', font=self.font)
        label.pack(anchor='center', expand=True)
        return frame
    
    def create_ansframe(self):
        frame =tk.Frame(self)
        self.set_bind(frame)
        self.anstxt = tk.StringVar(value='answer')
        self.anslabel = tk.Label(frame, textvariable=self.anstxt, font=self.font)   
        self.anslabel.pack(anchor='center',expand=True)
        self.set_bind(self.anslabel)
        return frame

    def create_intframe(self):
        frame = tk.Frame(self)
        return frame

    def run(self):
        while True:
            self.process()
    
    def process(self):
        self.update()

        self.labelstate = 'question'
        self.qframe.tkraise()
        time.sleep(2)
        self.labelstate = 'equal'
        self.eqframe.tkraise()
        time.sleep(1)
        self.labelstate = 'answer'
        self.ansframe.tkraise()
        self.thread_event.wait(1.5)
        self.labelstate = 'interval'
        self.intframe.tkraise()
        self.cleanup()
        time.sleep(1)

    def update(self):
        self.q = self.create_question()
        self.qtxt.set(f'{self.q[0]} {self.q[1]} {self.q[2]}')
        self.anstxt.set(self.q[3])

    def cleanup(self):
        self.records.append([self.level, *self.q, self.judgement])
        print(self.records[-1])
        self.thread_event.clear()
        self.level_change()
        self.clicked = False
        self.judgement = None

    
    def create_question(self):
        def adjust(ans):
            ans += sample([-1, 1], 1)[0] * int(sample(range(10), 1)[0])
            return ans
        
        def adjust2(ans):
            print(ans)
            n = len(str(abs(ans)))
            idx = randint(0, n-1)
            if str(abs(ans))[idx] == '9':
                op = -1
            elif str(abs(ans))[idx] == '0':
                op = 1
            else:
                op = sample([1, -1], 1)[0]
            ans += op * 10**idx
            print(ans)
            return ans
        
        op = sample(['+', '-'], 1)[0] # operator
        cw = random() # correct / wrong
        res = True

        if self.level == 1:
            num1 = randint(10, 100-1)
            num2 = randint(1, 10-1)
        elif self.level == 2:
            num1 = randint(10, 100-1)
            num2 = randint(10, 100-1)
        elif self.level == 3:
            num1 = randint(100, 1000-1)
            num2 = randint(10, 100-1)
            
        elif self.level == 4:
            num1 = randint(100, 1000-1)
            num2 = randint(100, 1000-1)
            op = '+'
        elif self.level == 5:
            num1 = randint(100, 1000-1)
            num2 = randint(100, 1000-1)
            op = '-'

        ans = eval(f'{num1}{op}{num2}')

        if cw <= 0.4: # create wrong answer
            ans = adjust2(ans)
            res = False
        
        q = [num1, op, num2, ans, res]
        return q

    def judge(self, q, ans):
        j = (q[-1] == ans)
        self.judgement = j

    def level_change(self):
        if self.judgement:
            if self.level < 5:
                self.level += 1
        else:
            if self.level > 1:
                self.level -= 1
        