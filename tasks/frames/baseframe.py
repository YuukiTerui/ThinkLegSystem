import tkinter as tk
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from ..apps.baseapp import BaseApp


class BaseFrame(tk.Frame):
    def __init__(self, master: BaseApp):
        super().__init__(master)
        self.logger = getLogger("gui.frame")
        self.master = master   
        self.bg = 'light gray'
        self.config(bg=self.bg)
        self.logger.debug("%sFrame is initialized.", self.__class__)

    def create_widgets(self):
        #self.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)
        self.grid(row=0, column=0, sticky="nsew")
    
    def finish(self):
        self.master.remove_frame()
        self.logger.debug("frame is destroied.")