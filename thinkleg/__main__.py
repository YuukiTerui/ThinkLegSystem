import os
import time
from threading import Thread, Event
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from tasks.apps import BaseApp
from tasks.frames import BaseFrame
from tasks.frames import VasFrame
from tasks.frames import TappingFrame
from tasks.frames import MentalCalcFrame
from tasks.frames import RestFrame
from arduino import Arduino
from manager import TimeManager


class ThinkLegApp(BaseApp):
    def __init__(self, datapath):
        self.logger = getLogger('thinkleg')
        self.datapath = datapath
        self.change_event = Event()

        self.arduino = Arduino(path=self.datapath, fname='arduino')
        self.arduino.start()

        super().__init__()
        self.title('ThinkLegTaskApp')
        self.first = FirstFrame(self)
        self.first.grid(row=0, column=0)
        self.time_manager = TimeManager(self)
        self.logger.debug('ThinkLegApp is initialized.')

    def __setattr__(self, name, value) -> None:
        if name == 'frame' and value == None:
            self.arduino.thinkleg_status = 'first'
            self.change_event.set()
            self.change_event.clear()
        return super().__setattr__(name, value)

    def set_frame(self, to, timelimit=None):
        self.logger.debug('set_frame is called.')
        self.arduino.thinkleg_status = to
        if to == 'vas':
            self.frame = VasFrame(self, self.datapath, 'vas.csv')
        elif 'mentalcalc' in to:
            self.frame = MentalCalcFrame(int(to[-1]), self, self.datapath, timelimit=timelimit)
        elif 'tapping' in to:
            self.frame = TappingFrame(int(to[-1]), self, self.datapath, timelimit=timelimit)
        elif 'rest' in to:
            self.frame = RestFrame(self, timelimit)

        self.frame.grid(row=0, column=0, sticky='nsew')

    def preliminary_exp(self):
        def process():
            frames = ['vas', 'tapping2', 'rest', 'vas', 'mentalcalc2', 'vas', 'mentalcalc2', 'vas', 'mentalcalc2', 'vas', 'tapping2', 'vas']
            #timelimits = [None, 300, 300, None, 1800, None, 1800, None, 1800, None, 300, None]
            timelimits = [None, 30, 30, None, 180, None, 180, None, 180, None, 30, None]
            for to, tl in zip(frames, timelimits):
                self.logger.info(f'pre {to}')
                self.set_frame(to, tl)
                self.change_event.wait()
        Thread(target=process, daemon=True).start()
        
    def finish(self):
        self.arduino.save('thinkleg')
        return super().finish()


class FirstFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.create_widgets()
        
    def create_widgets(self):
        self.grid(row=0, column=0, sticky='nsew')
        title_font = ('System', 90, 'bold', 'italic', 'underline', 'overstrike')
        self.title_label = tk.Label(self, text='Think Leg System', font=title_font)
        self.title_label.pack(pady=10, expand=True, fill=tk.X)

        self.task_frame = self.create_taskframe()
        self.task_frame.pack(pady=10)

        self.progress_frame = tk.Frame(self)
        self.progress_label = tk.Label(self.progress_frame, text='Preparing for Arduino')
        self.progress_label.pack()
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(self.progress_frame,
            orient=tk.HORIZONTAL, variable=self.progress_var, maximum=60, length=200, mode='determinate'
        )
        self.progress_bar.pack()
        self.progress_frame.pack()
        if self.master.arduino:
            Thread(target=self.__progress, daemon=True).start()
        
        self.finish_button = tk.Button(self, text='finish', width=20, height=5, command=lambda: self.master.finish())
        self.finish_button.pack(padx=50, pady=20, side=tk.BOTTOM, anchor=tk.SE)

        self.rest_button = tk.Button(self, text='Rest', width=20, height=5, command=lambda: self.set_frame('rest'))
        self.rest_button.pack(padx=50, pady=20, side=tk.BOTTOM, anchor=tk.SE)

        self.pre_exp_button = tk.Button(self, text='Pre_EXP', width=20, height=5, command=lambda: self.master.preliminary_exp())
        self.pre_exp_button.pack(padx=50, pady=20, side=tk.BOTTOM, anchor=tk.SE)
    
    def create_taskframe(self):
        frame = tk.LabelFrame(self, text='Tasks', font=('System', 40))
        padx = 50
        self.vas_frame = tk.LabelFrame(frame, text='VAS', font=('System', 30))
        self.tapping_frame = tk.LabelFrame(frame, text='Tapping', font=('System', 30))
        self.mentalcalc_frame = tk.LabelFrame(frame, text='MentalCalc', font=('System', 30))

        self.vas_frame.pack(padx=padx, side=tk.LEFT)
        self.tapping_frame.pack(padx=padx, side=tk.LEFT)
        self.mentalcalc_frame.pack(padx=padx, side=tk.LEFT)

        btn_w, btn_h = 10, 2
        self.vas_button = tk.Button(self.vas_frame, text='start', width=btn_w, height=btn_h, command=lambda:self.set_frame('vas'))
        self.vas_button.pack()

        self.radio_var_tapping = tk.IntVar(value=2)
        self.tapping_radio1 = tk.Radiobutton(self.tapping_frame, value=2, variable=self.radio_var_tapping, text='2')
        self.tapping_radio2 = tk.Radiobutton(self.tapping_frame, value=4, variable=self.radio_var_tapping, text='4')        
        self.tapping_radio1.pack()
        self.tapping_radio2.pack()
        self.tapping_button = tk.Button(self.tapping_frame, text='start', width=btn_w, height=btn_h,
            command=lambda:self.set_frame(f'tapping{self.radio_var_tapping.get()}', 30)
        )
        self.tapping_button.pack()

        self.radio_var_mentalcalc = tk.IntVar(value=2)
        self.mentalcalc_radio1 = tk.Radiobutton(self.mentalcalc_frame, value=2, variable=self.radio_var_mentalcalc, text='Low')
        self.mentalcalc_radio2 = tk.Radiobutton(self.mentalcalc_frame, value=4, variable=self.radio_var_mentalcalc, text='High')
        self.mentalcalc_radio1.pack()
        self.mentalcalc_radio2.pack()
        self.mentalcalc_button = tk.Button(self.mentalcalc_frame, text='start', width=btn_w, height=btn_h,
            command=lambda:self.set_frame(f'mentalcalc{self.radio_var_mentalcalc.get()}', 30)
        )
        self.mentalcalc_button.pack()
        return frame

    def __progress(self):
        st = time.time()
        latency = 60
        t = 0
        while t < latency:
            t = time.time()-st
            self.progress_var.set(t)
            time.sleep(1)
        self.progress_label['text'] = 'Arduino Ready.'
        self.progress_bar.destroy()

    def set_frame(self, to, timelimit=None):
        self.master.set_frame(to, timelimit)


def main():
    datapath = f'./data/{datetime.now().strftime("%Y%m%d/%H-%M-%S")}/'
    os.makedirs(datapath, exist_ok=True)

    app = ThinkLegApp(datapath)
    app.mainloop()



if __name__ == '__main__':
    main()
