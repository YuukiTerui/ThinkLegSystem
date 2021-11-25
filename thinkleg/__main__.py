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
from tasks.frames import NasaTLX
from tasks.frames import ATMTFrame
from tasks.frames import GoNoFrame
from tasks.frames import MATHFrame
from tasks.frames import PersonalityTestFrame
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

    def set_frame(self, to, timelimit=None, fname=None):
        self.logger.debug('set_frame is called.')
        self.arduino.thinkleg_status = to

        if to == 'vas':
            self.frame = VasFrame(self, path=self.datapath, fname='vas.csv')
        elif 'mentalcalc' in to:
            self.frame = MentalCalcFrame(int(to[-1]), self, self.datapath, fname=fname, timelimit=timelimit)
        elif 'tapping' in to:
            self.frame = TappingFrame(int(to[-1]), self, self.datapath,fname=fname, timelimit=timelimit)
        elif 'rest' in to:
            self.frame = RestFrame(self, timelimit)
        elif 'nasa_tlx' in to:
            self.frame = NasaTLX(self, path=self.datapath, fname=fname)
        elif 'atmt' in to:
            self.frame = ATMTFrame(self, path=self.datapath, fname=fname)
        elif 'math' in to:
            self.frame = MATHFrame(self, path=self.datapath, fname=fname, timelimit=timelimit)
        elif 'gono' in to:
            self.frame = GoNoFrame(self, fname=fname, path=self.datapath, timelimit=timelimit)
        elif 'personalitytest' in to:
            self.frame = PersonalityTestFrame(self, fname=fname, path=self.datapath)

        self.frame.grid(row=0, column=0, sticky='nsew')

    def preliminary_exp(self):
        def process():
            frames = ['vas', 'tapping4', 'rest', 'vas', 'mentalcalc4', 'vas', 'mentalcalc4', 'vas', 'mentalcalc4', 'vas', 'tapping4', 'vas', 'nasa_tlx']
            #timelimits = [None, 300, 300, None, 1800, None, 1800, None, 1800, None, 300, None, None]
            timelimits = [None, 10, 10, None, 20, None, 20, None, 20, None, 10, None, None]
            for to, tl in zip(frames, timelimits):
                self.logger.info(f'pre {to}')
                self.set_frame(to, tl)
                self.change_event.wait()
        Thread(target=process, daemon=True).start()

    def preliminary_exp2(self):
        def process():
            frames = 'rest vas mentalcalc4 atmt atmt atmt vas mentalcalc4 atmt atmt atmt vas mentalcalc4 atmt atmt atmt vas rest vas nasa_tlx nasa_tlx'.split()
            times = [60*3, None, 60*15, None, None, None, None, 60*15, None, None, None, None, 60*15, None, None, None, None, 60*3, None, None, None]
            #times = [60*0.1, None, 60*1, None, None, None, None, 60*1, None, None, None, None, 60*1, None, None, None, None, 60*0.1, None, None, None]
            fnames = [None, None, 'mentalcalc1', 'atmt1-1', 'atmt1-2', 'atmt1-3', None, 'mentalcalc2', 'atmt2-1', 'atmt2-2', 'atmt2-3', None, 'mentalcalc3', 'atmt3-1', 'atmt3-2', 'atmt3-3', None, None, None, 'nasa_calc', 'nasa_atmt']
            for to, tl, fn in zip(frames, times, fnames):
                self.logger.info(f'pre {to}')
                self.set_frame(to, timelimit=tl, fname=fn)
                self.change_event.wait()
        Thread(target=process, daemon=True).start()
        
    def preliminary_exp3(self): # nabetani
        ftf = [('vas', None, None), ('rest', 60*3, None), ('vas', None, None)] # (frame, time, fname)
        for i in range(1, 9):
            ftf.append((f'atmt', None, f'atmt1-{i}'))
            
        ftf.append(('vas', None, None))    
        ftf.append(('mentalcalc4', 60*15, 'mentalcalc1'))
        ftf.append(('vas', None, None))
        ftf.append(('mentalcalc4', 60*15, 'mentalcalc2'))
        ftf.append(('vas', None, None))
        ftf.append(('mentalcalc4', 60*15, 'mentalcalc3'))
        ftf.append(('vas', None, None))
        
        for i in range(1, 9):
            ftf.append((f'atmt', None, f'atmt2-{i}'))
        
        ftf.append(('vas', None, None))
        ftf.append(('rest', 60*3, None))
        ftf.append(('vas', None, None))
        ftf.append(('nasa_tlx', None, 'nasa_calc'))
        ftf.append(('nasa_tlx', None, 'nasa_atmt'))
        def process():
            for to, tl, fn in ftf:
                self.set_frame(to, timelimit=tl, fname=fn)
                self.change_event.wait()
        Thread(target=process, daemon=True).start()
            
    def main_exp(self):
        def process():
            gono = lambda n: ('gono', 3, f'gono{n}') # 180
            atmt = lambda n: ('atmt', 1, f'atmt{n}') # 180
            math = lambda n: ('math', 3, f'math{n}') # 180
            tasks = [gono, atmt, math]
            ftf = [('personalitytest', None, 'personalitytest'), ('vas', None, 'vas')]
            for i in range(3):
                for j in range(3):
                    ftf.append(tasks[j](f'{i+1}-{j+1}'))
                    if i != 2:
                        ftf.append(('vas', None, 'vas'))
                    else:
                        ftf.append(('nasa_tlx', None, f'nasa_{tasks[j].__name__}'))

            for frame, timelimit, fname in ftf:
                self.logger.info(f'main exp: {frame}')
                self.set_frame(frame, fname=fname, timelimit=timelimit)
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

        tabstyle = ttk.Style()
        tabstyle.theme_create( "MyStyle", parent="classic", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [50, 10],
                                        "font" : ('', '10', 'bold')},
                                        }})
        tabstyle.theme_use("MyStyle")

        self.tab = self.create_tabs()
        self.tab.pack(expand=True, anchor=tk.CENTER, fill=tk.Y)

        # self.task_frame = self.create_taskframe()
        # self.task_frame.pack(pady=10)

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

        #self.rest_button = tk.Button(self, text='Rest', width=20, height=5, command=lambda: self.set_frame('rest', 5))
        #self.rest_button.pack(padx=50, pady=20, side=tk.BOTTOM, anchor=tk.SE)
        #self.exp = lambda: self.master.preliminary_exp3()
        self.exp = lambda: self.master.main_exp()
        self.pre_exp_button = tk.Button(self, text='Pre_EXP', width=20, height=5, command=self.exp)
        self.pre_exp_button.pack(padx=50, pady=20, side=tk.BOTTOM, anchor=tk.SE)

    def create_tabs(self):
        tab = ttk.Notebook(self)
        self.create_vastab(tab)
        self.create_personalitytesttab(tab)
        self.create_gonotab(tab)
        self.create_atmttab(tab)
        self.create_mathtab(tab)
        self.create_nasatab(tab)
        return tab
        
    def create_mathtab(self, nb):
        btn_w, btn_h = 10, 2
        frame = tk.Frame(nb)
        exp = tk.Label(frame, text='MATH\n\n\
            ディスプレイ上に1~3桁の加算又は減算の式が2秒間提示されます．\n\
            その後，「EQUALS」という文字が1.5秒間提示されます．\n\
            さらに，計算式の答えの数値が2秒間提示されます．\n\
            答えが提示されている時間内に，提示された答えが正しいかどうか判断してください．\n\
            提示された答えが正しい場合はマウスを左クリック，間違っている場合はマウスを右クリックしてください．\n\
            回答が分からなかった場合はマウスをクリックしないでください．\n\
            以上の作業が所定の回数繰り返されます．')
        exp.pack()
        limit = tk.Entry(frame, width=10)
        limit.insert(tk.END, 10)
        limit.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h, command=lambda:self.set_frame('math', timelimit=int(limit.get())))
        start_btn.pack(pady=20, side=tk.BOTTOM)
        nb.add(frame, text='MATH')

    def create_gonotab(self, nb):
        btn_w, btn_h = 10, 2
        frame = tk.Frame(nb)
        exp = tk.Label(frame, text='選択反応課題\n\n\
            画面中央に上または下方向の矢印が0.2秒間提示されます．\n\
            その後，画面の中央を表す注視点が表示され，1.8秒後に注視点の上または下に黒い長方形が0.2秒間提示されます．\n\
            提示された矢印と長方形の上下の位置が一致した場合，可能な限り早くマウスを左クリックしてください．\n\
            以上の作業が所定の回数繰り返されます．')
        exp.pack()
        limit = tk.Entry(frame, width=10)
        limit.insert(tk.END, 10)
        limit.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h, command=lambda:self.set_frame('gono', timelimit=int(limit.get())))
        start_btn.pack(pady=20, side=tk.BOTTOM)
        nb.add(frame, text='GoNo')

    def create_vastab(self, nb):
        btn_w, btn_h = 10, 2
        frame = tk.Frame(nb)
        exp = tk.Label(frame, text='Visual Analog Scale\n\n主観的な疲労感を尋ねるスケールです．')
        exp.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h, command=lambda:self.set_frame('vas'))
        start_btn.pack(pady=20, side=tk.BOTTOM)
        nb.add(frame, text='VAS')

    def create_atmttab(self, nb):
        frame = tk.Frame(nb)
        btn_w, btn_h = 10, 2
        exp = tk.Label(frame, text='Advanced Trail Making Test(視覚探索課題)\n\n\
            画面上のランダムな位置に11から45の数の書かれた円形のマーカーがに表示されます．\n\
            11から45までの数の書かれたマーカーを順に，可能な限り早くクリックしてください．\n\
            クリックするたびに，表示される数の範囲が一つ大きくなり，マーカーの配置がランダムに変更されます．\n\
            次にクリックする必要のある数は画面の上部に表示されます．')
        exp.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h,
            command=lambda: self.set_frame(f'atmt'))
        start_btn.pack(pady=20, side=tk.BOTTOM)
        nb.add(frame, text='ATMT')

    def create_nasatab(self, nb):
        btn_w, btn_h = 10, 2
        frame = tk.Frame(nb)
        exp = tk.Label(frame, text='NASA-TLX\n\n\
            主観的なメンタルワークロード評価手法．\n\
            6つの下位尺度に関して，ワークロード(作業負担)の大きさを尋ねます．\n\
            一対比較を行う場合は，「どちらの指標が大きいかではなく，どちらの方が負担感に関連が深いか」を判断してください．')
        exp.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h,
                              command=lambda:self.set_frame(f'nasa_tlx'))
        start_btn.pack(pady=20, side=tk.BOTTOM)
        nb.add(frame, text='NASA-TLX')

    def create_personalitytesttab(self, nb):
        btn_w, btn_h = 10, 2
        frame = tk.Frame(nb)
        exp = tk.Label(frame, text='ニューカッスル・パーソナリティ評定尺度\n\n12項目の行動や考え方について回答することで，性格特性の評価をします．')
        exp.pack()
        start_btn = tk.Button(frame, text='Start', width=btn_w, height=btn_h,
            command=lambda: self.set_frame('personalitytest'))
        start_btn.pack(pady=20, side=tk.BOTTOM)
        nb.add(frame, text='PersonalityTest')


    def create_taskframe(self):
        frame = tk.LabelFrame(self, text='Tasks', font=('System', 40))
        padx = 50
        self.vas_frame = self.create_vas_frame(frame)
        self.vas_frame.pack(padx=padx, side=tk.LEFT)

        self.nasa_frame = self.create_nasatlx_frame(frame)
        self.nasa_frame.pack(padx=padx, side=tk.LEFT)

        self.math_frame = self.create_math_frame(frame)
        self.math_frame.pack(padx=padx, side=tk.LEFT)

        self.gono_frame = self.create_gono_frame(frame)
        self.gono_frame.pack(padx=padx, side=tk.LEFT)

        self.atmt_frame = self.create_atmt_frame(frame)
        self.atmt_frame.pack(padx=padx, side=tk.LEFT)

        #self.tapping_frame.pack(padx=padx, side=tk.LEFT)
        #self.tapping_frame = self.create_tapping_frame(frame)
        
        #self.mentalcalc_frame.pack(padx=padx, side=tk.LEFT)
        #self.mentalcalc_frame = self.create_mentalcalc_frame(frame)

        return frame

    def create_nasatlx_frame(self, master):
        frame = tk.LabelFrame(master, text='NASA-TLX', font=('System', 30))
        btn_w, btn_h = 10, 2
        self.start_btn = tk.Button(frame, text='start', width=btn_w, height=btn_h, command=lambda:self.set_frame('nasa_tlx'))
        self.start_btn.pack()
        return frame

    def create_math_frame(self, master):
        frame = tk.LabelFrame(master, text='MATH', font=('System', 30))
        btn_w, btn_h = 10, 2
        self.start_btn = tk.Button(frame, text='start', width=btn_w, height=btn_h, command=lambda:self.set_frame('math'))
        self.start_btn.pack()
        return frame

    def create_gono_frame(self, master):
        frame = tk.LabelFrame(master, text='GONO', font=('System', 30))
        btn_w, btn_h = 10, 2
        self.start_btn = tk.Button(frame, text='start', width=btn_w, height=btn_h, command=lambda:self.set_frame('gono'))
        self.start_btn.pack()
        return frame

    def create_atmt_frame(self, master):
        frame = tk.LabelFrame(master, text='ATMT', font=('System', 30))
        btn_w, btn_h = 10, 2
        self.start_btn = tk.Button(frame, text='start', width=btn_w, height=btn_h, command=lambda:self.set_frame('atmt'))
        self.start_btn.pack()
        return frame

    def create_vas_frame(self, master):
        frame = tk.LabelFrame(master, text='VAS', font=('System', 30))
        btn_w, btn_h = 10, 2
        self.vas_button = tk.Button(frame, text='start', width=btn_w, height=btn_h, command=lambda:self.set_frame('vas'))
        self.vas_button.pack()
        return frame

    def create_tapping_frame(self, master):
        frame = tk.LabelFrame(master, text='Tapping', font=('System', 30))
        btn_w, btn_h = 10, 2
        self.radio_var_tapping = tk.IntVar(value=2)
        self.tapping_radio1 = tk.Radiobutton(frame, value=2, variable=self.radio_var_tapping, text='2')
        self.tapping_radio2 = tk.Radiobutton(frame, value=4, variable=self.radio_var_tapping, text='4')        
        self.tapping_radio1.pack()
        self.tapping_radio2.pack()
        self.tapping_button = tk.Button(frame, text='start', width=btn_w, height=btn_h,
            command=lambda:self.set_frame(f'tapping{self.radio_var_tapping.get()}', 30)
        )
        self.tapping_button.pack()
        return frame

    def create_mentalcalc_frame(self, master):
        frame = tk.LabelFrame(master, text='MentalCalc', font=('System', 30))
        btn_w, btn_h = 10, 2

        self.radio_var_mentalcalc = tk.IntVar(value=2)
        self.mentalcalc_radio1 = tk.Radiobutton(frame, value=2, variable=self.radio_var_mentalcalc, text='Low')
        self.mentalcalc_radio2 = tk.Radiobutton(frame, value=4, variable=self.radio_var_mentalcalc, text='High')
        self.mentalcalc_radio1.pack()
        self.mentalcalc_radio2.pack()
        self.mentalcalc_button = tk.Button(frame, text='start', width=btn_w, height=btn_h,
            command=lambda:self.set_frame(f'mentalcalc{self.radio_var_mentalcalc.get()}', 30)
        )
        self.mentalcalc_button.pack()
        return frame

    def __progress(self):
        st = time.time()
        latency = 30
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
