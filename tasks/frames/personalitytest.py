import tkinter as tk
import json

from .baseframe import BaseFrame


class PersonalityTestFrame(BaseFrame):
    def __init__(self, master=None, fname='personalitytest', path='./'):
        super().__init__(master)
        self.path = path
        self.fname = fname

        self.qdata = self.load_json()
        print(self.qdata)

    def create_widgets(self):
        return
    
    def load_json(self):
        with open('./config/personality.json', 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
        return jsondata

