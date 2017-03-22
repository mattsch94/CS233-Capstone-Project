from tkinter import *

class Text:

    def __init__(self, tk, string):
        self.t = Label(tk)
        self.t['text'] = string

class Btn:

    def __init__(self, tk, string, command):
        self.b = Button(tk)
        self.b['text'] = string
        self.b['command'] = command

    def state(self, yn):
        if yn == FALSE:
            self.b['state'] = DISABLED
        else:
            self.b['state'] = NORMAL

class TxtBox:

    def __init__(self, tk):
        self.t = Entry(tk)

    def get_text(self):
        return self.t.get()

class List:

    def __init__(self, tk, mode=BROWSE):
        if mode == SINGLE:
            self.l = Listbox(tk, selectmode=mode)
        else:
            self.l = Listbox(tk)

    def get_choice(self):
        return self.l.get(self.l.curselection())

    def insert(self, string, item=END):
        self.l.insert(item, string)

    def delete(self, start, end):
        self.l.delete(start, end)

    def delete_all(self):
        self.l.delete(END, 0)
