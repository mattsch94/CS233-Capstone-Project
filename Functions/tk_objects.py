from tkinter import *

class Lbl:

    def __init__(self, tk, string):
        self.l = Label(tk)
        self.l['text'] = string

    def text(self, string):
        self.l['text'] = string

class Btn:

    def __init__(self, tk, string, command):
        self.b = Button(tk)
        self.b['text'] = string
        self.b['command'] = command

    def state(self, yn):
        if yn == FALSE:
            self.b.config(state=DISABLED)
        else:
            self.b.config(state=NORMAL)

    def command(self, cmd):
        self.b.config(command=cmd)

    def color(self, color):
        self.b.config(activeforeground=color)

class TxtBox:

    def __init__(self, tk):
        self.t = Entry(tk)

    def get_text(self):
        return self.t.get()

    def insert(self, text):
        self.t.insert(0, text)

    def password(self, hide):
        if hide:
            self.t.config(show='*')
        else:
            self.t.config(show='')

    def enable(self):
        self.t.config(state="normal")

    def disable(self):
        self.t.config(state="disabled")

class LargeTxtBox:

    def __init__(self, tk):
        self.l = Text(tk, wrap=WORD)

    def get_text(self):
        return self.l.get("1.0", "end-1c")

    def enable(self):
        self.l.configure(state="normal")

    def disable(self):
        self.l.configure(state="disabled")

    def insert(self, text):
        self.l.insert('1.0', text)

    def clear(self):
        self.l.delete('1.0', 'end')


class List:

    def __init__(self, tk, mode=BROWSE):
        if mode == SINGLE:
            self.l = Listbox(tk, selectmode=mode)
        else:
            self.l = Listbox(tk)

    def get_choice(self):
        get = self.l.curselection()
        if get:
            return self.l.get(get)
        else:
            return FALSE

    def insert(self, string, item=END):
        self.l.insert(item, string)

    def delete(self, start, end):
        self.l.delete(start, end)

    def delete_all(self):
        self.l.delete(0, END)

# Work in progress
class Calendar:

    def __init__(self, tk):
        self.w1d1 = Frame(tk, width=100, height=100)
        self.w1d2 = Frame(tk, width=100, height=100)
        self.w1d3 = Frame(tk, width=100, height=100)
        self.w1d4 = Frame(tk, width=100, height=100)
        self.w1d5 = Frame(tk, width=100, height=100)
        self.w1d6 = Frame(tk, width=100, height=100)
        self.w1d7 = Frame(tk, width=100, height=100)

        self.w2d1 = Frame(tk, width=100, height=100)
        self.w2d2 = Frame(tk, width=100, height=100)
        self.w2d3 = Frame(tk, width=100, height=100)
        self.w2d4 = Frame(tk, width=100, height=100)
        self.w2d5 = Frame(tk, width=100, height=100)
        self.w2d6 = Frame(tk, width=100, height=100)
        self.w2d7 = Frame(tk, width=100, height=100)

        self.w3d1 = Frame(tk, width=100, height=100)
        self.w3d2 = Frame(tk, width=100, height=100)
        self.w3d3 = Frame(tk, width=100, height=100)
        self.w3d4 = Frame(tk, width=100, height=100)
        self.w3d5 = Frame(tk, width=100, height=100)
        self.w3d6 = Frame(tk, width=100, height=100)
        self.w3d7 = Frame(tk, width=100, height=100)

        self.w4d1 = Frame(tk, width=100, height=100)
        self.w4d2 = Frame(tk, width=100, height=100)
        self.w4d3 = Frame(tk, width=100, height=100)
        self.w4d4 = Frame(tk, width=100, height=100)
        self.w4d5 = Frame(tk, width=100, height=100)
        self.w4d6 = Frame(tk, width=100, height=100)
        self.w4d7 = Frame(tk, width=100, height=100)

        self.w5d1 = Frame(tk, width=100, height=100)
        self.w5d2 = Frame(tk, width=100, height=100)
        self.w5d3 = Frame(tk, width=100, height=100)
        self.w5d4 = Frame(tk, width=100, height=100)
        self.w5d5 = Frame(tk, width=100, height=100)
        self.w5d6 = Frame(tk, width=100, height=100)
        self.w5d7 = Frame(tk, width=100, height=100)

    def grid(self, Row, Col):
        self.w1d1.grid(row=Row, col=Col)
        self.w1d2.grid(row=Row, col=Col+1)
        self.w1d3.grid(row=Row, col=Col+2)
        self.w1d4.grid(row=Row, col=Col+3)
        self.w1d5.grid(row=Row, col=Col+4)
        self.w1d6.grid(row=Row, col=Col+5)
        self.w1d7.grid(row=Row, col=Col+6)

        self.w2d1.grid(row=Row+1, col=Col)
        self.w2d2.grid(row=Row+1, col=Col+1)
        self.w2d3.grid(row=Row+1, col=Col+2)
        self.w2d4.grid(row=Row+1, col=Col+3)
        self.w2d5.grid(row=Row+1, col=Col+4)
        self.w2d6.grid(row=Row+1, col=Col+5)
        self.w2d7.grid(row=Row+1, col=Col+6)

        self.w3d1.grid(row=Row+2, col=Col)
        self.w3d2.grid(row=Row+2, col=Col+1)
        self.w3d3.grid(row=Row+2, col=Col+2)
        self.w3d4.grid(row=Row+2, col=Col+3)
        self.w3d5.grid(row=Row+2, col=Col+4)
        self.w3d6.grid(row=Row+2, col=Col+5)
        self.w3d7.grid(row=Row+2, col=Col+6)

        self.w4d1.grid(row=Row+3, col=Col)
        self.w4d2.grid(row=Row+3, col=Col+1)
        self.w4d3.grid(row=Row+3, col=Col+2)
        self.w4d4.grid(row=Row+3, col=Col+3)
        self.w4d5.grid(row=Row+3, col=Col+4)
        self.w4d6.grid(row=Row+3, col=Col+5)
        self.w4d7.grid(row=Row+3, col=Col+6)

        self.w5d1.grid(row=Row+4, col=Col)
        self.w5d2.grid(row=Row+4, col=Col+1)
        self.w5d3.grid(row=Row+4, col=Col+2)
        self.w5d4.grid(row=Row+4, col=Col+3)
        self.w5d5.grid(row=Row+4, col=Col+4)
        self.w5d6.grid(row=Row+4, col=Col+5)
        self.w5d7.grid(row=Row+4, col=Col+6)



