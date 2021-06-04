# coding: utf-8
import os
import time
import tkinter as tk


class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('BaseApp')
        self.width = 1200
        self.height = 800
        self.geometry(f'{self.width}x{self.height}')

        self.fullscreen_attr = '-fullscreen' if os.name == 'nt' else '-zoomed'    # nt -> windows, posix -> mac or linux
        self.fullscreen_state = False
        self.attributes(self.fullscreen_attr, self.fullscreen_state)

        self._init_key_binds()


    def _init_key_binds(self):
        self.bind('<F11>', self.toggle_fullscreen)
        self.bind('<F12>', self.quit_app)
        self.bind('<Escape>', self.quit_fullscreen)

    def toggle_fullscreen(self, event):
        self.fullscreen_state = not self.fullscreen_state
        self.attributes(self.fullscreen_attr, self.fullscreen_state)

    def quit_fullscreen(self, enent):
        self.fullscreen_state = False
        self.attributes(self.fullscreen_attr, self.fullscreen_state)

    def quit_app(self, event):
        self.finish()

    def finish(self):
        self.destroy()


class BaseFrame(tk.Frame):
    def __init__(self, master=None):
        self.master = BaseApp() if master == None else master
        super().__init__(master=self.master)
        self.bg = 'light gray'
        self.config(bg=self.bg)

        self.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)
        
    def finish(self):
        self.master.finish()


if __name__ == '__main__':
    app = BaseFrame()
    app.mainloop()