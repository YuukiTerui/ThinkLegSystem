import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

from .baseframe import BaseFrame
from ..apps.baseapp import BaseApp

class RestFrame(BaseFrame):
    def __init__(self, master: BaseApp, rest_time):
        super().__init__(master)
        self.rest_time = rest_time
        self.time_var = tk.IntVar(value=rest_time)
        self.create_widgets()
        Thread(target=self.__progress, daemon=True).start()
        

    def create_widgets(self):
        tk.Label(self).pack(fill=tk.Y, expand=True)
        self.label = tk.Label(self, text='休憩してください', font=('MSゴシック', 50, 'bold'))
        self.label.pack(pady=50, fill=tk.Y)
        self.bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, variable=self.time_var, maximum=self.rest_time, length=400, mode='determinate')
        self.bar.pack(pady=50)
        tk.Label(self).pack(fill=tk.Y, expand=True)
        return super().create_widgets()

    def __progress(self):
        while 0 < self.time_var.get():
            self.time_var.set(self.time_var.get() - 1)
            time.sleep(1)
        self.finish()
