from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *

class New_Session:
    
    def __init__(self):
        self.new_session = Toplevel(root)
        self.new_session.title('New Patient Session')
        self.new_session.geometry('600x600')

        self.ins1 = Lbl(self.new_session, 'Select patient and click next.')
        self.ins2 = Lbl(self.new_session, 'To add a new patient, go back and open Patient Manager.')

        self.pat_list = List(self.new_session, SINGLE)

        # INSERT CODE TO ALLOW PYTHON TO PULL PATIENTS FROM .db FILE.
        # ENSURE TO UTILIZE METHODS FOR RESETTING THE LIST UPON UPDATE.
        # DUMMY NAMES ARE CURRENTLY INSERTED TO TEST FUNCTIONALITY.

        connection = sqlite3.connect(db_address)
        cursor = connection.execute("SELECT ")

        # START DUMMY NAME CODE
        self.dummy_list = ['John Doe', 'Jane Doe', 'Ryan Baxter', 'Sarah Young', 'Miles Davis',
                           'Eddie Reyes', 'George West', 'Katherine White', 'Peggy Morris',
                           'Sam Jack', 'Queenie Davis', 'Killian Jones', 'Katy Duds']
        for name in self.dummy_list:
            self.pat_list.insert(name)
        # END DUMMY NAME CODE

        self.back = Btn(self.new_session, 'Back', self.back_btn_a)
        self.nxt = Btn(self.new_session, 'Next', self.next_btn)

    def next_btn(self):
        self.name = self.pat_list.get_choice()
        if self.name:
            self.__init_window_two__()
            self.launch_window_two()
            self.new_session.destroy()
        else:
            showerror('Error', 'Please select a patient to continue.')

    def back_btn_a(self):
        self.new_session.destroy()

    def back_btn_b(self):
        self.note_session.destroy()

    def launch_window_one(self):
        self.ins1.l.grid(row=0, column=1)
        self.pat_list.l.grid(row=1, column=1)
        self.ins2.l.grid(row=2, column=1)
        self.back.b.grid(row=3, column=0)
        self.nxt.b.grid(row=3, column=3)

    def __init_window_two__(self):
        self.note_session = Toplevel(root)
        self.ins3 = Lbl(self.note_session, 'Type session notes below. Then click Submit.')
        msg_template = 'Current Patient: xyzz'
        msg_display = string.replace(msg_template, 'xyzz', str(self.pat_list.get_choice()))
        self.ins4 = Lbl(self.note_session, str(msg_display))

        self.notes = LargeTxtBox(self.note_session)

        self.cncl = Btn(self.note_session, 'Cancel', self.back_btn_b)
        self.sbmt = Btn(self.note_session, 'Submit', self.back_btn_b)  # Create "submit" fxn when database is set up.

    def launch_window_two(self):
        self.ins3.l.grid(row=0, column=1)
        self.ins4.l.grid(row=1, column=1)
        self.notes.l.grid(row=2, column=1)
        self.cncl.b.grid(row=3, column=0)
        self.sbmt.b.grid(row=3, column=2)

def launch_new_session():
    window = New_Session()
    window.launch_window_one()
    mainloop()
