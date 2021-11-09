# coding: utf-8
import time
import tkinter as tk
from threading import Thread, Event
import numpy as np
from random import random, randint, sample, uniform
from datetime import datetime

from .baseframe import BaseFrame


class GoNoFrame(BaseFrame):
    def __init__(self, master=None, fname=None, path='./'):
        super().__init__(master)
        self.path = path
        self.fname = fname
        
        self.clicked = None
        self.font = ('', 100, 'bold')
        self.create_widgets()

        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()
        self.thread_event = Event()

    def set_bind(self, obj):
        obj.bind('<Button-1>', self.mouse_clicked)
    
    def mouse_clicked(self, event):
        pass

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
        tk.Label(frame, text='+', font=self.font).pack(anchor=tk.CENTER, expand=True)
        return frame

    def create_s2_frame(self):
        frame = tk.Frame(self)
        self.upper_label = tk.Label(frame, bg='red')
        self.upper_label.pack(anchor=tk.S, expand=True)
        tk.Label(frame, text='+', font=self.font).pack(anchor=tk.CENTER, expand=True)
        self.bottom_label = tk.Label(frame, bg='black')
        self.bottom_label.pack(anchor=tk.N, expand=True)
        return frame


    def run(self):
        while True:
            self.process()
    
    def process(self):
        self.update()
        self.s1_frame.tkraise()
        #time.sleep(0.2)
        time.sleep(1)
        self.mid_frame.tkraise()
        time.sleep(1.8)
        self.s2_frame.tkraise()
        #time.sleep(0.2)
        time.sleep(1)
        self.mid_frame.tkraise()
        time.sleep(uniform(2.6, 2.8))

    def update(self) -> None:
        target_rate = random()
        target = sample(['↑', '↓'], 1)[0]
        self.s1_var.set(target)
        if 0.8 <= target_rate:
            if target == '↑':
                self.upper_label.config(bg='black')
                self.bottom_label.config(bg='gray94')
            else:
                self.upper_label.config(bg='gray94')
                self.bottom_label.config(bg='black')
        else:
            if target == '↑':
                self.upper_label.config(bg='gray94')
                self.bottom_label.config(bg='black')
            else:
                self.upper_label.config(bg='black')
                self.bottom_label.config(bg='gray94')
