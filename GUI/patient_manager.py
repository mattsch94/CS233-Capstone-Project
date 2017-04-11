from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *
from Functions.std_functions import *
import string

class pat_manager:

    class editor:

        def __init__(self, id_num=NONE, fname=NONE, lname=NONE, bday=NONE, address=NONE, phone=NONE):
            self.edit = Toplevel(root)
            self.edit.title('Patient Editor')
            self.edit.geometry('600x300')

            self.insA = Lbl(self.edit, 'Add/Update patient details and then click submit.')
            self.insB = Lbl(self.edit, 'All fields are required.')

            self.cancel = Btn(self.edit, 'Cancel', NONE)
            self.submit = Btn(self.edit, 'Submit', NONE)

            self.nameA = Lbl(self.edit, 'First Name: ')
            self.nameB = TxtBox(self.edit)
            self.nameC = Lbl(self.edit, 'Last Name: ')
            self.nameD = TxtBox(self.edit)
            self.bdayA = Lbl(self.edit, 'Birthday: ')
            self.bdayB = TxtBox(self.edit)
            self.bdayC = Lbl(self.edit, 'MM/DD/YYYY')
            self.addressA = Lbl(self.edit, 'Address: ')
            self.addressB = TxtBox(self.edit)
            self.phoneA = Lbl(self.edit, 'Phone Number: ')
            self.phoneB = TxtBox(self.edit)
            self.phoneC = Lbl(self.edit, 'ex: 1234567890 (No Dashes)')

            self.fname = fname
            self.lname = lname
            self.bday = bday
            self.address = address
            self.phone = phone
            self.id_num = id_num

            self.edit_bool = FALSE

        def launch_blank(self):
            #self.insA.l.grid(row=0, column=1)
            #self.insB.l.grid(row=1, column=1)
            self.nameA.l.grid(row=3, column=0)
            self.nameB.t.grid(row=3, column=1)
            self.nameC.l.grid(row=4, column=0)
            self.nameD.t.grid(row=4, column=1)
            self.bdayA.l.grid(row=5, column=0)
            self.bdayB.t.grid(row=5, column=1)
            self.bdayC.l.grid(row=5, column=2)
            self.addressA.l.grid(row=6, column=0)
            self.addressB.t.grid(row=6, column=1)
            self.phoneA.l.grid(row=7, column=0)
            self.phoneB.t.grid(row=7, column=1)
            self.phoneC.l.grid(row=7, column=2)

        def launch_edit(self):
            if self.fname is not NONE:
                self.nameB.insert(self.fname)
            if self.lname is not NONE:
                self.nameD.insert(self.lname)
            if self.bday is not NONE:
                self.bdayB.insert(self.bday)
            if self.address is not NONE:
                self.addressB.insert(self.address)
            if self.phone is not NONE:
                self.phoneB.insert(self.phone)
            self.edit_bool = TRUE
            self.launch_blank()

        def cancel(self):
            if askyesno('Cancel', 'Are you sure you want to cancel?'):
                self.edit.destroy()

        def empty_id(self):
            connection = sqlite3.connect(db_address)
            id_list = connection.execute('SELECT id FROM patients;').fetchall()
            match_id = 1

            for number in id_list:
                if number == match_id:
                    match_id += 1
                else:
                    return match_id

            return match_id

        def submit(self):
            ID = self.id_num
            FNAME = self.nameB.get_text()
            LNAME = self.nameD.get_text()
            BDAY = self.bdayB.get_text()
            ADDRESS = self.addressB.get_text()
            PHONE = self.phoneB.get_text()

            connection = sqlite3.connect(db_address)

            if self.edit_bool is FALSE:
                ID = self.empty_id()
            else:
                connection.execute("DELETE FROM patients WHERE id='%s'") % ID

            connection.execute("INSERT INTO patients VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
                               % (ID, FNAME, LNAME, BDAY, ADDRESS, PHONE))
            connection.commit()

    def __init__(self):
        self.manager = Toplevel(root)
        self.manager.title('Patient Manager')
        self.manager.geometry("600x600")

        self.ins1 = Lbl(self.manager, 'Select a patient and then a command. Or select Add Patient.')

        self.pat_list = List(self.manager, SINGLE)

        self.update_list()

        self.new = Btn(self.manager, 'New Patient', self.new_patient)
        self.edit = Btn(self.manager, 'Edit Patient', self.edit_patient)
        self.delete = Btn(self.manager, 'Delete Patient', NONE)

    def update_list(self):
        self.pat_list.delete_all()
        connection = sqlite3.connect(db_address)
        cursor = connection.execute('SELECT fname, lname FROM patients;')
        for row in cursor:
            first = row[0]
            last = row[1]
            full_name = first + " " + last
            self.pat_list.insert(full_name)
        connection.close()

    def new_patient(self):
        launcher = self.editor()
        launcher.launch_blank()

    def edit_patient(self):
        if self.pat_list.get_choice():
            full_name = self.pat_list.get_choice()
            split_name = str(full_name).split()
            first = split_name[0]
            last = split_name[1]

            connection = sqlite3.connect(db_address)
            cursor = connection.execute("SELECT * FROM patients WHERE fname='%s' AND lname='%s'").fetchall() % (first, last)

            launcher = self.editor(cursor[0], cursor[1], cursor[2], cursor[3], cursor[4], cursor[5])
            launcher.launch_edit()
        else:
            showerror('Error', 'Please select a patient to continue.')

    def launch(self):
        self.ins1.l.grid(row=0, column=1)
        self.pat_list.l.grid(row=1, column=1)
        self.new.b.grid(row=2, column=0)
        self.edit.b.grid(row=2, column=1)
        self.delete.b.grid(row=2, column=3)

def launch_manager():
    window = pat_manager()
    window.launch()





