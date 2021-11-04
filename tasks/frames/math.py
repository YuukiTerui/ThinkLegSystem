# coding: utf-8
import csv
import time
import tkinter as tk
import numpy as np
from numpy.random import randint, normal, choice
from datetime import datetime

from .baseframe import BaseFrame


class MATHFrame(BaseFrame):
    def __init__(self, master=None, fname=None, path='./'):
        super().__init__(master)
        self.path = path
        self.fname = fname
        
        self.create_widgets()
        self.init_bind(self)
        
    def init_bind(self, obj):
        obj.bind('<Button-1>', self.mouse_clicked)
        obj.bind('<Button-3>', self.mouse_clicked)
        
    def mouse_clicked(self, event):
        pass
    
    def create_widgets(self):
        self.qframe = self.create_qframe()
        self.
        self.eqframe = self.create_eqframe()
        self.ansframe = self.create_ansframe()
        
        
    def create_qframe(self):
        frame = tk.Frame(self)
        
    
    def create_eqframe(self):
        pass
    
    def create_ansframe(self):
        pass
    
    def roop(self):
        pass
    
    def update(self):
        pass
    