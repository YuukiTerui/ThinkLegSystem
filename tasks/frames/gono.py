# coding: utf-8
import csv
import time
import tkinter as tk
from threading import Thread, Event
from random import random, choice, uniform
from datetime import datetime

from .baseframe import BaseFrame


class GoNoFrame(BaseFrame):
    def __init__(self, master=None, fname=None, path='./', timelimit=None):
        super().__init__(master)
        self.path = path
        self.fname = fname
        
        self.is_clicked = False
        self.records = []
        self.record = None
        self.font = ('', 100, 'bold')
        self.create_widgets()

        self.timelimit = timelimit
        self.ptimes = 0
        self.thread_event = Event()
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()
        

    def set_bind(self, obj):
        obj.bind('<Button-1>', self.mouse_clicked)
    
    def mouse_clicked(self, event):
        if self.is_clicked:
            return
        ans_t = datetime.now() - self.s_time
        self.record.append(ans_t.total_seconds())
        if self.record[-2]:
            if self.record[-1] > 0.5: # 
                self.record.append(False)
            else:
                self.record.append(True)
        else:
            self.record.append(False)
        self.is_clicked = True

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.s1_frame = self.create_s1_frame()
        self.mid_frame = self.create_mid_frame()
        self.s2_frame = self.create_s2_frame()

        self.s1_frame.grid(row=0, column=0, sticky='nsew')
        self.mid_frame.grid(row=0, column=0, sticky='nsew')
        self.s2_frame.grid(row=0, column=0, sticky='nsew')
        return

    def create_s1_frame(self):
        frame = tk.Frame(self)
        self.s1_var = tk.StringVar(value='↑')
        self.s1_label = tk.Label(frame, textvariable=self.s1_var, font=self.font)
        self.s1_label.pack(anchor=tk.CENTER, expand=True)
        return frame

    def create_mid_frame(self):
        frame = tk.Frame(self)
        self.set_bind(frame)
        label = tk.Label(frame, text='+', font=self.font)
        label.pack(anchor=tk.CENTER, expand=True)
        self.set_bind(label)
        return frame

    def create_s2_frame(self):
        frame = tk.Frame(self)
        self.set_bind(frame)
        self.upper_label = tk.Label(frame, bg='red', width=50, height=10)
        self.upper_label.pack(anchor=tk.S, expand=True)
        self.set_bind(self.upper_label)
        self.center_label = tk.Label(frame, text='+', font=self.font)
        self.center_label.pack(anchor=tk.CENTER, expand=True)
        self.set_bind(self.center_label)
        self.bottom_label = tk.Label(frame, bg='black', width=50, height=10)
        self.bottom_label.pack(anchor=tk.N, expand=True)
        self.set_bind(self.bottom_label)
        return frame

    def run(self):
        if self.timelimit:
            while self.ptimes < self.timelimit:
                self.process()
        else:
            while True:
                self.process()
    
    def process(self):
        self.update()
        self.s1_frame.tkraise()
        time.sleep(0.2)
        #time.sleep(1)
        self.mid_frame.tkraise()
        time.sleep(1.8)
        self.s2_frame.tkraise()
        self.s_time = datetime.now()
        time.sleep(0.2)
        #time.sleep(2)
        self.mid_frame.tkraise()
        time.sleep(uniform(2.6, 2.8))
        self.cleanup()

    def update(self) -> None:
        self.target_rate = random()
        self.target = choice(['↑', '↓'])
        self.s1_var.set(self.target)
        if self.target_rate <= 0.8: # correct rate: 0.8
            if self.target == '↑':
                self.upper_label.config(bg='black')
                self.bottom_label.config(bg='gray94')
            else:
                self.upper_label.config(bg='gray94')
                self.bottom_label.config(bg='black')
        else:
            if self.target == '↑':
                self.upper_label.config(bg='gray94')
                self.bottom_label.config(bg='black')
            else:
                self.upper_label.config(bg='black')
                self.bottom_label.config(bg='gray94')
        self.record = [self.target, self.target_rate<=0.8]

    def cleanup(self):
        if len(self.record) == 2:
            self.record.append(None)
            self.record.append((self.target_rate<=0.8) == self.is_clicked)
        self.is_clicked = False
        self.records.append(self.record)
        self.logger.info(self.records[-1])

    def save(self):
        if '.csv' not in self.fname:
            self.fname += '.csv'
        with open(self.path + self.fname, 'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(self.records)
        self.logger.info('gono records is saved.: %s', self.fname)

    def exit_process(self):
        self.save()
        self.finish()