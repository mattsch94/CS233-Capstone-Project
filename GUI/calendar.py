from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *

class Appointment:

    def __init__(self):
        self.window = Toplevel(root)
        self.window.title('Appointment Calendar')
        # self.window.geometry('700x700')

        self.d_text = Lbl(self.window, '               Date: ')
        self.d_entry = TxtBox(self.window)
        self.d_submit = Btn(self.window, 'Submit', None)

        self.appt_list = List(self.window)
        self.new_appt = Btn(self.window, 'New Appointment', None)
        self.edit_appt = Btn(self.window, 'Edit Appointment', None)
        self.del_appt = Btn(self.window, 'Delete Appointment', None)

        self.close = Btn(self.window, 'Close', self.window.destroy)

        self.d_text.l.grid(row=0, column=0)
        self.d_entry.t.grid(row=0, column=1, columnspan=1)
        self.d_submit.b.grid(row=0, column=2)
        self.appt_list.l.grid(row=1, column=1, columnspan=1)
        self.new_appt.b.grid(row=2, column=0)
        self.edit_appt.b.grid(row=2, column=1)
        self.del_appt.b.grid(row=2, column=2)
        self.close.b.grid(row=2, column=3)
