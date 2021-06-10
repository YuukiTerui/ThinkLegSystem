import tkinter as tk

from .baseframe import BaseFrame


class MainFrame(BaseFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text='Think Leg System')
        self.title_label.pack()

        self.vas_button = tk.Button(self, text='vas', command=lambda:self.change_frame('vas'))
        self.vas_button.pack()

        self.calc_button = tk.Button(self, text='calc', command=lambda:self.change_frame('calc'))
        self.calc_button.pack()

        self.finish_button = tk.Button(self, text='finish', command=lambda: self.master.finish())
        self.finish_button.pack()

    def change_frame(self, to):
        self.master.change_frame(to)