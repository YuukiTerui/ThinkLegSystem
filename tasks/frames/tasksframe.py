import tkinter as tk

from .baseframe import BaseFrame


class TasksFrame(BaseFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        title_font = ('System', 100, 'bold', 'italic', 'underline', 'overstrike')
        self.title_label = tk.Label(self, text='Think Leg System', font=title_font)
        self.title_label.pack(pady=10, expand=True, fill=tk.X)

        self.task_frame = self.create_taskframe()
        self.task_frame.pack(pady=10)
        
        self.finish_button = tk.Button(self, text='finish', width=20, height=5, command=lambda: self.master.finish())
        self.finish_button.pack(padx=50, pady=50, side=tk.BOTTOM, anchor=tk.SE)
    
    def create_taskframe(self):
        frame = tk.LabelFrame(self, text='Tasks', font=('System', 60))
        padx = 50
        self.vas_frame = tk.LabelFrame(frame, text='VAS', font=('System', 30))
        self.calc_frame = tk.LabelFrame(frame, text='Calc', font=('System', 30))
        self.mentalcalc_frame = tk.LabelFrame(frame, text='MentalCalc', font=('System', 30))
        self.stroop_frame = tk.LabelFrame(frame, text='Stroop', font=('System', 30))

        self.vas_frame.pack(padx=padx, side=tk.LEFT)
        self.calc_frame.pack(padx=padx, side=tk.LEFT)
        self.mentalcalc_frame.pack(padx=padx, side=tk.LEFT)
        self.stroop_frame.pack(padx=padx, side=tk.LEFT)

        btn_w, btn_h = 10, 2
        self.vas_button = tk.Button(self.vas_frame, text='start', width=btn_w, height=btn_h, command=lambda:self.change_frame('vas'))
        self.vas_button.pack()

        self.calc_button = tk.Button(self.calc_frame, text='start', width=btn_w, height=btn_h, command=lambda:self.change_frame('calc'))
        self.calc_button.pack()

        self.radio_var_mentalcalc = tk.IntVar(value=2)
        self.mentalcalc_radio1 = tk.Radiobutton(self.mentalcalc_frame, value=2, variable=self.radio_var_mentalcalc, text='Low')
        self.mentalcalc_radio2 = tk.Radiobutton(self.mentalcalc_frame, value=4, variable=self.radio_var_mentalcalc, text='High')
        self.mentalcalc_radio1.pack()
        self.mentalcalc_radio2.pack()
        self.mentalcalc_button = tk.Button(self.mentalcalc_frame, text='start', width=btn_w, height=btn_h,
            command=lambda:self.change_frame(f'mentalcalc{self.radio_var_mentalcalc.get()}')
        )
        self.mentalcalc_button.pack()

        self.radio_var_stroop = tk.IntVar(value=1)
        self.stroop_radio1 = tk.Radiobutton(self.stroop_frame, value=1, variable=self.radio_var_stroop, text='task1')
        self.stroop_radio2 = tk.Radiobutton(self.stroop_frame, value=2, variable=self.radio_var_stroop, text='task2')
        self.stroop_radio3 = tk.Radiobutton(self.stroop_frame, value=3, variable=self.radio_var_stroop, text='task3')
        self.stroop_radio4 = tk.Radiobutton(self.stroop_frame, value=4, variable=self.radio_var_stroop, text='task4')
        self.stroop_radio1.pack()
        self.stroop_radio2.pack()
        self.stroop_radio3.pack()
        self.stroop_radio4.pack()

        self.stroop_button = tk.Button(self.stroop_frame, text='start', width=btn_w, height=btn_h, 
            command=lambda: self.change_frame(f'stroop{self.radio_var_stroop.get()}')
        )
        self.stroop_button.pack()
        return frame

    def change_frame(self, to):
        self.master.change_frame(to)