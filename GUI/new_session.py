from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *
from Functions.db_functions import *

class New_Session:
    
    def __init__(self):
        self.new_session = Toplevel(root)
        self.new_session.title('New Patient Session')
        # self.new_session.geometry('500x250')

        self.ins1 = Lbl(self.new_session, 'Select patient and click next.')
        self.ins2 = Lbl(self.new_session, 'To add a new patient, go back and open Patient Manager.')

        self.pat_list = List(self.new_session, SINGLE)

        self.master_list = Patient_List()
        for patient in self.master_list.pList:
            self.pat_list.insert(patient.full_name())

        self.back = Btn(self.new_session, 'Close', self.back_btn_a)
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

    def back_btn_b(self, ask=TRUE):
        if ask:
            if askyesno('Confirm', 'Are you sure you want to cancel?'):
                self.note_session.destroy()
        else:
            self.note_session.destroy()

    def submit_btn(self):

        if askyesno('Confirm', 'Are you sure you want to save? Notes cannot be edited after being saved.'):
            notes = self.notes.get_text()
            pat_id = self.master_list.id(str(self.name))

            time = Time_Stamp()

            connection = sqlite3.connect(db_address)
            connection.executescript(pragma.query)
            sql_stmt = ('INSERT INTO notes VALUES (' + str(pat_id) + ', "' + str(time.y_m_d) + '", "' + str(time.h_m_s)
                        + '", "' + str(notes) + '");')
            connection.execute(sql_stmt)
            connection.commit()

            showinfo('Saved', 'Session notes were successfully saved.')

            self.back_btn_b(FALSE)


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
        self.sbmt = Btn(self.note_session, 'Save', self.submit_btn)

    def launch_window_two(self):
        self.ins3.l.grid(row=0, column=1)
        self.ins4.l.grid(row=1, column=1)
        self.notes.l.grid(row=2, column=1)
        self.cncl.b.grid(row=3, column=0)
        self.sbmt.b.grid(row=3, column=2)

def launch_new_session():
    connection = sqlite3.connect(db_address)
    connection.executescript(pragma.query)
    sql_cmd = 'SELECT patient_id FROM patients;'
    cursor = connection.execute(sql_cmd).fetchall()
    if cursor == []:
        showerror('Error', 'There must be at least one patient in the database to start a new session.')
    else:
        window = New_Session()
        window.launch_window_one()
        mainloop()
