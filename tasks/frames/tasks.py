import tkinter as tk
from tkinter import ttk

from .baseframe import BaseFrame
from ..frames import VasFrame


class TasksFrame(BaseFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        title_font = ('URW Gothic L', 100, 'bold', 'italic', 'underline', 'overstrike')
        self.title_label = tk.Label(self, text='Think Leg System', font=title_font)
        self.title_label.pack(pady=10, expand=True, fill=tk.X)

        tabstyle = ttk.Style()
        tabstyle.theme_create( "MyStyle", parent="classic", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [50, 10],
                                        "font" : ('', '10', 'bold')},
                                        }})
        tabstyle.theme_use("MyStyle")
        
        
        self.tab = self.create_tabs()
        self.tab.pack(expand=True, anchor=tk.CENTER, fill=tk.Y)
        
        
        
        self.finish_button = tk.Button(self, text='finish', width=20, height=5, command=lambda: self.master.finish())
        self.finish_button.pack(padx=50, pady=50, side=tk.BOTTOM, anchor=tk.SE)
    
    def create_tabs(self):
        tab = ttk.Notebook(self)

        self.create_vastab(tab)
        self.create_mathtab(tab)
        self.create_calctab(tab)
        self.create_mentalcalctab(tab)
        self.create_typingtab(tab)
        self.create_strooptab(tab)
        self.create_atmttab(tab)
        self.create_nasatab(tab)
        return tab
    
    def create_mathtab(self, nb):
        btn_w, btn_h = 10, 2
        frame = tk.Frame(nb)
        exp = tk.Label(frame, text='MATH\n')
        exp.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h, command=lambda:self.change_frame('math'))
        start_btn.pack(anchor=tk.CENTER, expand=True)
        nb.add(frame, text='MATH')

    def create_vastab(self, nb):
        btn_w, btn_h = 10, 2
        frame = tk.Frame(nb)
        exp = tk.Label(frame, text='Visual Analog Scale\n')
        exp.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h, command=lambda:self.change_frame('vas'))
        start_btn.pack(anchor=tk.CENTER, expand=True)
        nb.add(frame, text='VAS')

    def create_calctab(self, nb):
        frame = tk.Frame(nb)
        btn_w, btn_h = 10, 2
        self.calc_button = tk.Button(frame, text='start', width=btn_w, height=btn_h, command=lambda:self.change_frame('calc'))
        self.calc_button.pack(anchor=tk.CENTER, expand=True)
        nb.add(frame, text='Calc')

    def create_mentalcalctab(self, nb):
        frame = tk.Frame(nb)
        btn_w, btn_h = 10, 2
        self.radio_var_mentalcalc = tk.IntVar(value=2)
        self.mentalcalc_radio1 = tk.Radiobutton(frame, value=2, variable=self.radio_var_mentalcalc, text='Low')
        self.mentalcalc_radio2 = tk.Radiobutton(frame, value=4, variable=self.radio_var_mentalcalc, text='High')
        self.mentalcalc_radio1.pack()
        self.mentalcalc_radio2.pack()
        self.mentalcalc_button = tk.Button(frame, text='Start', width=btn_w, height=btn_h,
            command=lambda:self.change_frame(f'mentalcalc{self.radio_var_mentalcalc.get()}')
        )
        self.mentalcalc_button.pack()
        nb.add(frame, text='MentalCalc')

    def create_typingtab(self, nb):
        frame = tk.Frame(nb)
        btn_w, btn_h = 10, 2
        self.radio = tk.IntVar(value=2)
        self.radio_btn1 = tk.Radiobutton(frame, value=2, variable=self.radio, text='2')
        self.radio_btn2 = tk.Radiobutton(frame, value=4, variable=self.radio, text='4')        
        self.radio_btn1.pack()
        self.radio_btn2.pack()
        self.start_btn = tk.Button(frame, text='start', width=btn_w, height=btn_h,
            command=lambda:self.change_frame(f'tapping{self.radio.get()}')
        )
        self.start_btn.pack(anchor=tk.SE)
        nb.add(frame, text='Typing')

    def create_strooptab(self, nb):
        frame = tk.Frame(nb)
        btn_w, btn_h = 10, 2
        radio = tk.IntVar(value=1)
        self.radio_btn1 = tk.Radiobutton(frame, value=1, variable=radio, text='task1')
        self.radio_btn2 = tk.Radiobutton(frame, value=2, variable=radio, text='task2')
        self.radio_btn3 = tk.Radiobutton(frame, value=3, variable=radio, text='task3')
        self.radio_btn4 = tk.Radiobutton(frame, value=4, variable=radio, text='task4')
        self.radio_btn1.pack()
        self.radio_btn2.pack()
        self.radio_btn3.pack()
        self.radio_btn4.pack()

        self.start_btn = tk.Button(frame, text='start', width=btn_w, height=btn_h, 
            command=lambda: self.change_frame(f'stroop{radio.get()}')
        )
        self.start_btn.pack()
        nb.add(frame, text='Stroop')

    def create_atmttab(self, nb):
        frame = tk.Frame(nb)
        btn_w, btn_h = 10, 2
        
        self.start_btn = tk.Button(frame, text='start', width=btn_w, height=btn_h,
            command=lambda: self.change_frame(f'atmt'))
        self.start_btn.pack()
        nb.add(frame, text='ATMT')

    def create_nasatab(self, nb):
        frame = tk.Frame(nb)
        self.start_btn = tk.Button(frame, text='Start', 
                              command=lambda:self.change_frame(f'nasa_tlx'))
        self.start_btn.pack(pady=10)
        nb.add(frame, text='NASA-TLX')

    def change_frame(self, to):
        self.master.change_frame(to)