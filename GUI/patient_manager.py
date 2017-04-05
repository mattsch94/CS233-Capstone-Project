from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *

class pat_manager:

    class editor:

        def __init__(self, fname=NONE, lname=NONE, bday=NONE, address=NONE, phone=NONE):
            self.edit = Toplevel(root)
            self.edit.title('Patient Editor')
            self.edit.geometry('300x300')

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

            self.edit_bool = FALSE

        def launch_blank(self):
            self.insA.l.grid(row=0, col=0)
            self.insB.l.grid(row=1, col=0)
            self.nameA.l.grid(row=3, col=0)
            self.nameB.t.grid(row=3, col=1)
            self.nameC.l.grid(row=4, col=0)
            self.nameD.t.grid(row=4, col=1)
            self.bdayA.l.grid(row=5, col=0)
            self.bdayB.t.grid(row=5, col=1)
            self.bdayC.l.grid(row=5, col=2)
            self.addressA.l.grid(row=6, col=0)
            self.addressB.t.grid(row=6, col=2)
            self.phoneA.l.grid(row=7, col=0)
            self.phoneB.t.grid(row=7, col=1)
            self.phoneC.l.grid(row=7, col=2)

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

        def submit(self):
            FNAME = self.nameB.get_text()
            LNAME = self.nameD.get_text()
            BDAY = self.bdayB.get_text()
            ADDRESS = self.addressB.get_text()
            PHONE = self.phoneB.get_text()
            connection = sqlite3.connect(db_address)

            if self.edit_bool is FALSE:
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

        self.new = Btn(self.manager, 'New Patient', NONE)
        self.edit = Btn(self.manager, 'Edit Patient', NONE)
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
        self.

