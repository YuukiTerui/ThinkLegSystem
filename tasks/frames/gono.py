# coding: utf-8
import time
import tkinter as tk
from threading import Thread, Event
import numpy as np
from random import random, randint, sample
from datetime import datetime

from .baseframe import BaseFrame


class GoNo(BaseFrame):
    def __init__(self, master=None, fname=None, path='./'):
        self.path = path
        self.fname = fname
        
        self.clicked = None
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
        self.mid_frame = tk.Frame(self, )
        self.s2_frame = tk.Frame(self, )

        self.s1_frame.grid(row=0, column=0, sticky='nsew')
        self.mid_frame.grid(row=0, column=0, sticky='nsew')
        self.s2_frame.grid(row=0, column=0, sticky='nsew')

        return

    def create_s1_frame(self):
        frame = tk.Frame(self)
        self.s1_var = tk.StringVar()
        self.s1_label = tk.Label(frame, textvariable=self.s1_var)
        return frame

    def create_mid_frame(self):
        frame = tk.Frame(self)
        tk.Label(frame, text='+').pack(anchor=tk.CENTER)
        return frame

    def create_s2_frame(self):
        frame = tk.Frame(self)

    def run(self):
        while True:
            self.process()
    
    def process(self):
        self.s1_frame.tkraise()
        time.sleep(2)
        self.mid_frame.tkraise()
        time.sleep(2)
        self.s2_frame.tkraise()
        time.sleep(2)



