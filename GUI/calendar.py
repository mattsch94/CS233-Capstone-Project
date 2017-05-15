from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *
from Functions.db_functions import *

class Calendar:

    def __init__(self):
        self.window = Toplevel(root)
        self.window.title('Appointment Calendar')
        # self.window.geometry('700x700')

        self.d_text = Lbl(self.window, '               Date: ')
        self.d_entry = TxtBox(self.window)
        self.d_submit = Btn(self.window, 'Submit', self.populate_list)
        self.d_today = Btn(self.window, 'Today', self.populate_list_today)

        self.appt_list = List(self.window)
        self.appt_list.l.config(width=45)
        self.new_appt = Btn(self.window, 'New Appointment', self.new_appt)
        self.edit_appt = Btn(self.window, 'Edit Appointment', self.edit_appt)
        self.del_appt = Btn(self.window, 'Delete Appointment', self.delete_appt)

        self.close = Btn(self.window, 'Close', self.window.destroy)

        self.d_text.l.grid(row=0, column=0)
        self.d_entry.t.grid(row=0, column=1, columnspan=1)
        self.d_submit.b.grid(row=0, column=2)
        self.d_today.b.grid(row=0, column=3)
        self.appt_list.l.grid(row=1, column=0, columnspan=4)
        self.new_appt.b.grid(row=2, column=0)
        self.edit_appt.b.grid(row=2, column=1)
        self.del_appt.b.grid(row=2, column=2)
        self.close.b.grid(row=2, column=3)

        self.active_date = None

    def populate_list_today(self):
        date_db = Time_Stamp()
        self.d_entry.clear()
        self.d_entry.insert(str(date_convert(db=date_db.y_m_d)))
        self.populate_list()

    def date_error(self):
        msg = 'Please enter a date in "MM/DD/YYYY" format, including a preceding 0 if necessary'
        showerror('Error', msg)

    def date_entry_verify(self, date):
        dt = str(date)

        if len(dt) != 10:
            return False

        if not dt[0:2].isdigit():
            return False

        if not dt[2:3] == '/':
            return False

        if not dt[3:5].isdigit():
            return False

        if not dt[5:6] == '/':
            return False

        if not dt[6:10].isdigit():
            return False

        if int(dt[0:2]) < 1 or int(dt[0:2]) > 12:
            return False

        if int(dt[3:5]) < 1 or int(dt[3:5]) > 31:
            return False

        if int(dt[6:10]) < 1:
            return False

        return True

    def populate_list(self):

        self.appt_list.delete_all()

        if self.d_entry.get_text():
            date = self.d_entry.get_text()
            self.active_date = date
        else:
            self.date_error()
            return

        if self.date_entry_verify(date):
            db_date = date_convert(proper=date)
        else:
            self.date_error()
            return

        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")
        sql_cmd = ('SELECT p.lname || ", " || p.fname AS name, c.start_time, c.end_time ' +
                   'FROM calendar c ' +
                   'INNER JOIN patients p ' +
                   'ON c.patient_id = p.patient_id ' +
                   'WHERE c.date = ' + db_date + ' ' +
                   'ORDER BY c.start_time;')
        cursor = connection.execute(sql_cmd).fetchall()

        for appointment in cursor:
            self.appt_list.insert(str(appointment[0]) + ' - ' +
                                  str(time_convert(db=appointment[1])[:5]) + ' to ' +
                                  str(time_convert(db=appointment[2])[:5]))

        connection.close()

    def delete_appt(self):
        if self.appt_list.get_choice():
            msg = 'Are you sure you want to delete this appointment?'
            if askyesno('Confirm', msg):
                appt = str(self.appt_list.get_choice())
                lname = str(appt.split()[0][:-1])
                fname = str(appt.split()[1])
                start = str(time_convert(proper=appt.split()[3]))
                end = str(time_convert(proper=appt.split()[5]))
                date = str(date_convert(proper=self.active_date))

                connection = sqlite3.connect(db_address)
                connection.executescript("pragma key='x41gq'")
                sql_cmd_1 = 'SELECT patient_id FROM patients WHERE fname="' + fname + '" AND lname="' + lname + '";'
                cursor = connection.execute(sql_cmd_1).fetchone()
                pat_id = str(cursor[0])

                sql_cmd_2 = ('DELETE FROM calendar WHERE patient_id=' + pat_id + ' AND date="' + date +
                             '" AND start_time="' + start + '" AND end_time="' + end + '";')
                connection.execute(sql_cmd_2)
                connection.commit()
                connection.close()
                self.appt_list.delete_all()
        else:
            msg = 'Please select an appointment to continue.'
            showerror('Error', msg)

    def new_appt(self):
        if self.active_date is None:
            showerror('Error', 'Please select a date to create an appointment.')
        else:
            Appointment(self.active_date)
            self.appt_list.delete_all()

    def edit_appt(self):
        if self.active_date is None or not self.d_entry.get_text():
            showerror('Error', 'Please select a date and patient to edit an appointment.')
        else:
            appt = str(self.appt_list.get_choice())
            name = str(appt.split()[0]) + ' ' + str(appt.split()[1])
            start = str(appt.split()[3])
            end = str(appt.split()[5])

            Appointment(self.active_date, name, start, end)
            self.appt_list.delete_all()

class Appointment:

    def __init__(self, date, patient=None, start=None, end=None):

        self.window = Toplevel(root)
        self.window.title('Appointment Editor')
        # self.window.geometry('500x500')

        options = ['<Select a Patient>']

        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")
        sql_cmd = 'SELECT lname || ", " || fname FROM patients ORDER BY lname;'
        cursor = connection.execute(sql_cmd).fetchall()

        for name in cursor:
            options.append(name[0])

        self.variable = StringVar(self.window)
        self.variable.set(options[0])

        connection.close()

        self.drop_down = apply(OptionMenu, (self.window, self.variable) + tuple(options))

        self.date_text = Lbl(self.window, 'Appointment Date:')
        self.start_text = Lbl(self.window, 'Appointment Start:')
        self.end_text = Lbl(self.window, 'Appointment End:')

        self.date_display = TxtBox(self.window)
        self.date_display.insert(str(date))
        self.date_display.disable()

        self.start_entry = TxtBox(self.window)
        self.end_entry = TxtBox(self.window)

        self.submit = Btn(self.window, 'Submit', self.submit)
        self.cancel = Btn(self.window, 'Cancel', self.cancel)

        self.edit = False

        if patient and start and end:

            index = 0
            for name in options:
                if patient == name:
                    break
                else:
                    index += 1

            self.variable.set(options[index])
            self.drop_down.config(state=DISABLED)

            self.start_entry.insert(str(start))
            self.end_entry.insert(str(end))

            self.edit = True

            self.old_start = str(start)
            self.old_end = str(end)

        self.drop_down.grid(row=0, column=0, columnspan=2)
        self.date_text.l.grid(row=1, column=0)
        self.date_display.t.grid(row=1, column=1)
        self.start_text.l.grid(row=2, column=0)
        self.start_entry.t.grid(row=2, column=1)
        self.end_text.l.grid(row=3, column=0)
        self.end_entry.t.grid(row=3, column=1)
        self.submit.b.grid(row=4, column=0)
        self.cancel.b.grid(row=4, column=1)

    def cancel(self):
        if askyesno('Cancel', 'Are you sure you want to cancel?'):
            self.window.destroy()

    def time_error(self):
        msg = 'Please enter time in 24-Hour HH:MM format.'
        showerror('Error', msg)

    def time_verify(self, time):
        tm = str(time)

        if len(tm) == 4:
            tm = str('0' + tm)
        elif len(tm) != 5:
            self.time_error()
            return False

        if not tm[0:2].isdigit():
            self.time_error()
            return False

        if not tm[2:3] == ':':
            self.time_error()
            return False

        if not tm[3:5].isdigit():
            self.time_error()
            return False

        if int(tm[0:2]) < 0 or int(tm[0:2]) > 23:
            self.time_error()
            return False

        if int(tm[3:5]) < 0 or int(tm[3:5]) > 59:
            self.time_error()
            return False

        return True

    def submit(self):

        # Establish Database Connection
        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")

        # Collect Entries
        name = str(self.variable.get())
        start = str(self.start_entry.get_text())
        end = str(self.end_entry.get_text())
        date = str(self.date_display.get_text())

        fname = str(name.split()[1])
        lname = str(name.split()[0][:-1])

        # Verify Times - Submit is cancelled if verification fails.
        if not self.time_verify(start):
            return
        if not self.time_verify(end):
            return

        # Obtain Database-Ready Values
        sql_cmd = 'SELECT patient_id FROM patients WHERE fname="' + fname + '" AND lname="' + lname + '";'
        cursor = connection.execute(sql_cmd).fetchone()
        pat_id = str(cursor[0])

        db_date = str(date_convert(proper=date))
        db_start = str(time_convert(proper=start))
        db_end = str(time_convert(proper=end))

        # Delete Old Entry if Editing Appointment
        if self.edit:
            db_old_start = time_convert(proper=self.old_start)
            db_old_end = time_convert(proper=self.old_end)

            sql_cmd = ('DELETE FROM calendar WHERE patient_id=' + pat_id + ' AND date="' + db_date +
                       '" AND start_time="' + db_old_start + '" AND end_time="' + db_old_end + '";')
            connection.execute(sql_cmd)
            connection.commit()

        # Insert New Entry into Database
        sql_cmd = ('INSERT INTO calendar VALUES (' + pat_id + ', "' + db_date + '", "' + db_start +
                   '", "' + db_end + '");')
        connection.execute(sql_cmd)
        connection.commit()

        # Closing Commands
        showinfo('Success', 'The appointment was scheduled successfully.')
        connection.close()
        self.window.destroy()
