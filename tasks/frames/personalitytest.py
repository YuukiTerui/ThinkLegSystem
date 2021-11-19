import tkinter as tk
from tkinter import messagebox
import json

from .baseframe import BaseFrame


class PersonalityTestFrame(BaseFrame):
    def __init__(self, master=None, fname='personalitytest', path='./'):
        super().__init__(master)
        self.path = path
        self.fname = fname

        self.qdata = self.load_json()
        self.title = self.qdata['タイトル']
        self.introduction = self.qdata['説明']
        self.scales = self.qdata['尺度']
        self.questions = self.qdata['質問']
        self.qnum = 1 # 1 ~ 12
        self.qstr = tk.StringVar(value=f'{self.questions[str(self.qnum)]["question"]} ({self.qnum}/12)')
        self.qans = [None] * 12

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text=self.title, font=('', 30, 'bold'))
        self.title_label.pack(pady=(180,50))

        self.intro_label = tk.Label(self, text=self.introduction, font=('', 15, ''))
        self.intro_label.pack(pady=30)

        self.scale_frame = tk.Frame(self)
        for i in range(5, 0, -1):
            tk.Label(self.scale_frame, text=f'{i}.{self.scales[str(i)]}',
                    font=('', 15, '')).pack(padx=20, side=tk.LEFT)
        self.scale_frame.pack()

        self.centerframe = tk.Frame(self)
        self.centerframe.pack(pady=(100, 10))

        self.question_label = tk.Label(self.centerframe, textvariable=self.qstr, font=('', 30, ''))
        self.question_label.pack(anchor=tk.N)

        self.radio_frame = tk.Frame(self.centerframe)
        self.radio_value = tk.IntVar()
        for i in range(5, 0, -1):
            tk.Radiobutton(self.radio_frame, text=i, value=i, font=('', 20, 'bold'),
                            variable=self.radio_value,
                            command=self.radio_clicked
                            ).pack(padx=20, side=tk.LEFT)
        self.radio_frame.pack()
        self.back_button = tk.Button(self.centerframe, text='前の質問に戻る', 
                                    font=('', 15, ''), command=self.previous_question)
        self.back_button.pack(side=tk.LEFT, pady=10)
        self.go_button = tk.Button(self.centerframe, text='次の質問に進む',
                                    font=('', 15, ''), command=self.next_question)
        self.go_button.pack(side=tk.RIGHT, pady=10)

        self.submit_button = tk.Button(self, text='提出する', font=('', 20, ''), command=self.submit)
        self.submit_button.pack(expand=True)
        return

    def radio_clicked(self):
        value = self.radio_value.get() # 1 ~ 5
        reverse = self.questions[str(self.qnum)]['reverse'] # true/false
        self.qans[self.qnum-1] = value if not reverse else 6 - value
        self.logger.info(self.qans)
    
    def next_question(self):
        if self.radio_value.get() == 0:
            messagebox.showwarning('Warning', '質問に回答してください')
            return 
        if self.qnum < 12:
            self.qnum += 1
            self.qstr.set(f'{self.questions[str(self.qnum)]["question"]} ({self.qnum}/12)')
            if self.qans[self.qnum-1] == None: # 次に表示する質問に未回答のとき
                self.radio_value.set(0) # ラジオボタンのチェックを外す
            else: # 既に回答していた場合
                self.radio_value.set(self.qans[self.qnum-1]) #その回答のボタンにチェックをいれる
    def previous_question(self):
        if self.qnum > 1:
            self.qnum -= 1
            self.radio_value.set(self.qans[self.qnum-1])
            self.qstr.set(self.questions[str(self.qnum)]['question'])

    def submit(self):
        if None in self.qans:
            messagebox.showerror('Error', '全ての項目に回答してください')
            return
        if messagebox.askyesno('提出確認', '提出してよろしいですか？'):
            self.save()
            self.finish()

    def save(self):
        self.logger.info(f'saved answer: {self.qans}')
        score = self.calc_score()
        self.logger.info(f'score {score}')
        exp = self.explain(score)
        self.logger.info(f'explanation {exp}')

        if '.json' not in self.fname:
            self.fname += '.json'
        with open(self.path + self.fname, encoding='utf-8', mode='w') as f:
            json.dump({'回答':self.qans, 'スコア':score, '解釈':exp}, f, ensure_ascii=False, indent=4)

    def load_json(self):
        with open('./config/personality.json', 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
        return jsondata

    def calc_score(self):
        scales = self.qdata['次元']
        score = {}
        for k, idxs in self.qdata['計算'].items():
            score[k] = sum([self.qans[i-1] for i in idxs])
        return score

    def explain(self, score:dict):
        exp = self.qdata['解釈']
        result = {}
        for k, v in score.items():
            for e, rng in exp[k].items():
                if v in rng:
                    result[k] = e
                    break
        return result