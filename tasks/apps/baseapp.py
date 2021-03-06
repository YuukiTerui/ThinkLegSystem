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

        self.frame = None

        self.geometry(f'{self.width}x{self.height}')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.fullscreen_attr = '-fullscreen'# if os.name == 'nt' else '-zoomed'    # nt -> windows, posix -> mac or linux
        self.fullscreen_state = True
        self.attributes(self.fullscreen_attr, self.fullscreen_state)

        self._init_key_binds()
        self.logger.debug("BaseApp is initialized.")

    def _init_key_binds(self):
        self.bind('<F11>', self.toggle_fullscreen)
        #self.bind('<F12>', self.quit_app)
        self.bind('<Tab>', (lambda: 'pass')())
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

    def remove_frame(self):
        if isinstance(self.frame, tk.Frame):
            self.frame.destroy()
        self.frame = None
            

    def finish(self):
        self.destroy()
        self.logger.info("BaseApp is finished.")


if __name__ == '__main__':
    from ..frames.baseframe import BaseFrame

    app = BaseFrame()
    app.logger.info("app is running")
    app.mainloop()