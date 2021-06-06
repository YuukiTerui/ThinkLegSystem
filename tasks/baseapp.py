# coding: utf-8
import os
import time
import tkinter as tk
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))


class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logger = getLogger('gui.app')
        self.title('BaseApp')
        self.width = 1200
        self.height = 800
        self.geometry(f'{self.width}x{self.height}')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.fullscreen_attr = '-fullscreen' if os.name == 'nt' else '-zoomed'    # nt -> windows, posix -> mac or linux
        self.fullscreen_state = False
        self.attributes(self.fullscreen_attr, self.fullscreen_state)

        self._init_key_binds()
        self.logger.warning("BaseApp is initialized.")

    def _init_key_binds(self):
        self.bind('<F11>', self.toggle_fullscreen)
        self.bind('<F12>', self.quit_app)
        self.bind('<Escape>', self.quit_fullscreen)
        self.logger.debug("key binds are initialized.")

    def toggle_fullscreen(self, event):
        self.fullscreen_state = not self.fullscreen_state
        self.attributes(self.fullscreen_attr, self.fullscreen_state)
        self.logger.info("toggle_fullscreen is called.")

    def quit_fullscreen(self, enent):
        self.fullscreen_state = False
        self.attributes(self.fullscreen_attr, self.fullscreen_state)
        self.logger.info("quit_fullscreen is called.")

    def quit_app(self, event):
        self.finish()
        self.logger.info("quit_app is called.")

    def finish(self):
        self.destroy()
        self.logger.info("BaseApp is finished.")


class BaseFrame(tk.Frame):
    def __init__(self, master=None):
        self.logger = getLogger("gui.frame")
        self.master = BaseApp() if master == None else master
        super().__init__(master=self.master)
        self.bg = 'light gray'
        self.config(bg=self.bg)
        #self.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)
        self.grid(row=0, column=0, sticky="nsew")
        self.logger.debug("%sFrame is initialized.", self.__class__)

    def finish(self):
        self.destroy()
        self.logger.debug("frame is destroied.")


if __name__ == '__main__':
    app = BaseFrame()
    app.logger.info("app is running")
    app.mainloop()