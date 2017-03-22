from tkinter import *

class Text:

    def __init__(self, tk):
        self.lbl = Label(tk)

    def text(self, string):
        self.lbl['text'] = string

class Btn:

    def __init__(self, tk, string, command):
        self.btn = Button(tk)
        self.btn['text'] = string
        self.btn['command'] = command

    def state(self, yn):
        if yn == FALSE:
            self.btn['state'] = DISABLED
        else:
            self.btn['state'] = NORMAL
