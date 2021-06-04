import tkinter as tk
from tasks.baseapp import BaseApp, BaseFrame
from tasks.vas import VasFrame


class MainApp(BaseApp):
    def __init__(self):
        super().__init__()
        self.state = 0
        self.frame = None
        self.create_widgets()

    def create_widgets(self):
        self.frame = BaseFrame(self)
        self.frame.pack()

        self.title_label = tk.Label(self.frame, text='Think Leg System')
        self.title_label.pack()

        self.vas_button = tk.Button(self.frame, text='vas', command=self.create_vas)
        self.vas_button.pack()

    def create_vas(self):
        pass




def main():
    app = MainApp()
    app.mainloop()



if __name__ == '__main__':
    main()
