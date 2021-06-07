import os
from datetime import datetime
import tkinter as tk
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))
    
from tasks.baseapp import BaseApp, BaseFrame
from tasks.vas import VasFrame
from tasks.calc import CalcFrame


class MainApp(BaseApp):
    def __init__(self, datapath):
        super().__init__()
        self.datapath = datapath
        self.state = 0
        self.frame = None
        self.create_widgets()

    def create_widgets(self):
        self.first_frame = BaseFrame(self)
        self.first_frame.grid(row=0, column=0, sticky="nsew")

        self.title_label = tk.Label(self.first_frame, text='Think Leg System')
        self.title_label.pack()

        self.vas_button = tk.Button(self.first_frame, text='vas', command=lambda:self.change_frame('vas'))
        self.vas_button.pack()

        self.calc_button = tk.Button(self.first_frame, text='calc', command=lambda:self.change_frame('calc'))
        self.calc_button.pack()

    def create_vas(self):
        self.frame = VasFrame(self, path=self.datapath, fname='vas.csv')
        self.frame.grid(row=0, column=0, sticky="nsew")

    def create_calc(self):
        self.frame = CalcFrame(self, path=self.datapath, fname='calc.csv')
        self.frame.grid(row=0, column=0, sticky="nsew")

    def change_frame(self, to):
        #self.first_frame.pack_forget()
        if self.frame:
            self.frame.destroy()
        if to == 'vas':
            self.create_vas()
        elif to == 'calc':
            self.create_calc()
            




def main():
    datapath = f'./data/{datetime.now().strftime("%Y%m%d/%H-%M-%S")}/'
    print(datapath)
    os.makedirs(datapath, exist_ok=True)

    app = MainApp(datapath)
    app.mainloop()



if __name__ == '__main__':
    main()