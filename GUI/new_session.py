from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *
from Functions.db_functions import *
import datetime

class New_Session:
    
    def __init__(self):
        self.new_session = Toplevel(root)
        self.new_session.title('New Patient Session')
        self.new_session.geometry('600x600')

        self.ins1 = Lbl(self.new_session, 'Select patient and click next.')
        self.ins2 = Lbl(self.new_session, 'To add a new patient, go back and open Patient Manager.')

        self.pat_list = List(self.new_session, SINGLE)

        self.master_list = Patient_List()
        for patient in self.master_list.pList:
            self.pat_list.insert(patient.full_name())

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
        if askyesno('Confirm', 'Are you sure you want to cancel?'):
            self.note_session.destroy()

    def submit_btn(self):

        if askyesno('Confirm', 'Are you sure you want to submit? Notes cannot be edited after being submitted.'):
            notes = self.notes.get_text()
            pat_id = self.master_list.id(str(self.name))
            i = datetime.datetime.now()
            year = i.year
            month = i.month
            day = i.day

            year_s = str(year)

            if month < 10:
                month_s = '0' + str(month)
            else:
                month_s = str(month)

            if day < 10:
                day_s = '0' + str(day)
            else:
                day_s = str(day)

            y_m_d = year_s + month_s + day_s

            connection = sqlite3.connect(db_address)
            sql_stmt = ('INSERT INTO notes VALUES (' + str(pat_id) + ', ' + str(y_m_d) + ', "' + str(notes)
                        + '");')
            connection.execute(sql_stmt)
            connection.commit()

            showinfo('Saved', 'Session notes were successfully saved.')

            self.back_btn_b()


    def launch_window_one(self):
        self.ins1.l.grid(row=0, column=1)
        self.pat_list.l.grid(row=1, column=1)
        self.ins2.l.grid(row=2, column=1)
        self.back.b.grid(row=3, column=0)
        self.nxt.b.grid(row=3, column=3)


    def __init_window_two__(self):
        self.note_session = Toplevel(root)
        self.ins3 = Lbl(self.note_session, 'Type session notes below. Then click Submit.')
        msg = 'Current Patient: ' + str(self.pat_list.get_choice())
        self.ins4 = Lbl(self.note_session, str(msg))

        self.notes = LargeTxtBox(self.note_session)

        self.cncl = Btn(self.note_session, 'Cancel', self.back_btn_b)
        self.sbmt = Btn(self.note_session, 'Submit', self.submit_btn)  # Create "submit" fxn when database is set up.

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
