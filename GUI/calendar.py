from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *

class Appointment:

    def __init__(self):
        self.appointment = Toplevel(root)
        self.appointment.title('Appointment Calendar')
        self.appointment.geometry('700x700')

