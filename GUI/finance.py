from root_file import *
from Functions.tk_objects import *
from tkinter.messagebox import *
from Functions.db_functions import *
import datetime

class Finance_Manager:

    def __init__(self):

        self.window = Toplevel(root)
        self.window.title('Finance Manager')
        # self.window.geometry('500x500')

        self.pat_list = List(self.window)
        self.open = Btn(self.window, 'Open Account', self.launch_acct_mgr)
        self.refresh = Btn(self.window, 'Refresh List', self.update_list)
        self.close = Btn(self.window, 'Close Window', self.window.destroy)

        self.manager = Patient_List()
        self.update_list()

        self.pat_list.l.grid(row=0, column=0, columnspan=3)
        self.open.b.grid(row=1, column=0)
        self.refresh.b.grid(row=1, column=1)
        self.close.b.grid(row=1, column=2)

    def update_list(self):
        del self.manager
        self.manager = Patient_List()
        self.pat_list.delete_all()

        max_no = 0
        for patient in self.manager.pList:
            self.pat_list.insert(patient.full_name())
            max_no += 1

        id_list = []
        for patient in self.manager.pList:
            id_list.append(patient.id_num)

        cur_no = 0
        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")

        while cur_no < max_no:
            sql_cmd = 'SELECT SUM(charge) FROM finance WHERE patient_id=' + str(id_list[cur_no]) +';'
            cursor = connection.execute(sql_cmd).fetchone()
            if cursor[0] == None or int(cursor[0]) == 0:
                self.pat_list.l.itemconfig(cur_no, {'fg':'green'})
            elif cursor[0] > 0:
                self.pat_list.l.itemconfig(cur_no, {'fg':'blue'})
            else:
                self.pat_list.l.itemconfig(cur_no, {'fg':'red'})
            cur_no += 1

    def launch_acct_mgr(self):
        if self.pat_list.get_choice():
            name = str(self.pat_list.get_choice())
            pat_id = self.manager.id(name)
            Account_Manager(pat_id, name)
        else:
            showerror('Error', 'Please select a patient to continue.')

class Account_Manager:

    def __init__(self, patient_id, patient_name):

        self.window = Toplevel(root)
        self.window.title('Account Manager')
        # self.window.geometry('500x500')

        self.pat_id = patient_id
        self.pat_name = patient_name

        name_msg = 'Current Account: ' + str(self.pat_name)
        self.name_lbl = Lbl(self.window, name_msg)
        self.bal_label = Lbl(self.window, None)
        self.balance = None
        self.update_balance()

        self.transaction = Frame(self.window, borderwidth=3, relief='groove', padx=10, pady=10)
        self.txn_lbl = Lbl(self.transaction, 'Transaction')
        self.dollar_lbl_left = Lbl(self.transaction, 'Amount: $')
        self.dollar_amt = TxtBox(self.transaction)
        self.dollar_lbl_right = Lbl(self.transaction, '.00')
        self.charge = Btn(self.transaction, 'Charge', self.charge)
        self.payment = Btn(self.transaction, 'Payment', self.payment)

        self.view_acct = Btn(self.window, 'View Account', self.launch_view_acct)
        self.close = Btn(self.window, 'Close Window', self.window.destroy)

        self.name_lbl.l.grid(row=0, column=0, columnspan=2)
        self.bal_label.l.grid(row=1, column=0, columnspan=2)
        self.transaction.grid(row=2, column=0, columnspan=2)

        self.txn_lbl.l.grid(row=0, column=0, columnspan=4)
        self.dollar_lbl_left.l.grid(row=1, column=0, columnspan=2)
        self.dollar_amt.t.grid(row=1, column=3)
        self.dollar_lbl_right.l.grid(row=1, column=4)
        self.charge.b.grid(row=2, column=0, columnspan=2)
        self.payment.b.grid(row=2, column=3, columnspan=2)

        self.view_acct.b.grid(row=3, column=0)
        self.close.b.grid(row=3, column=1)

    def update_balance(self):
        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")
        sql_cmd = 'SELECT SUM(charge) FROM finance WHERE patient_id=' + str(self.pat_id) + ';'
        cursor = connection.execute(sql_cmd).fetchone()

        if cursor[0] == None:
            bal = 0
        else:
            bal = cursor[0]

        self.balance = 'Current Balance: $' + str(bal) + '.00'
        self.bal_label.text(self.balance)
        connection.close()

    def add_transaction(self, amount):
        time = Time_Stamp()

        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")
        sql_cmd = ('INSERT INTO finance VALUES (' + str(self.pat_id) + ', "' + str(time.y_m_d) + '", "' +
                   str(time.h_m_s) + '", ' + str(amount) + ');')
        connection.execute(sql_cmd)
        connection.commit()
        connection.close()

    def charge(self):
        get = self.dollar_amt.get_text()
        if get and str(get).isdigit() and 0 < int(get) < 1000000:
            amount = int(get)
            confirm = ('Please confirm that you want to charge the account of ' + str(self.pat_name) + ' in the ' +
                        'amount of $' + str(amount) + '.00.')
            if askyesno('Confirm Charge', confirm):
                self.add_transaction(amount * -1)
                self.update_balance()
                self.dollar_amt.clear()
        else:
            error = 'Please enter a whole number greater than 1 and less than 1,000,000 to perform a transaction.'
            showerror('Error', error)

    def payment(self):
        get = self.dollar_amt.get_text()
        if get and str(get).isdigit() and 0 < int(get) < 1000000:
            amount = int(self.dollar_amt.get_text())
            confirm = ('Please confirm that you want apply a payment to the account of ' + str(self.pat_name) +
                        ' in the amount of $' + str(amount) + '.00.')
            if askyesno('Confirm Payment', confirm):
                self.add_transaction(amount)
                self.update_balance()
                self.dollar_amt.clear()
        else:
            error = 'Please enter a whole number greater than 1 and less than 1,000,000 to perform a transaction.'
            showerror('Error', error)

    def launch_view_acct(self):
        Account(self.pat_id, self.pat_name, self.balance)

class Account:

    def __init__(self, patient_id, patient_name, balance):

        self.window = Toplevel(root)
        self.window.title('Account Details')
        # self.window.geometry('500x500')

        self.name = patient_name
        self.id = patient_id
        self.bal = balance

        self.details = LargeTxtBox(self.window)
        self.details.disable()
        self.close = Btn(self.window, 'Close Window', self.window.destroy)

        self.populate_account()

        self.details.l.grid(row=0, column=0)
        self.close.b.grid(row=1, column=0)

    def populate_account(self):

        time = Time_Stamp()

        title = ('Account details for ' + str(self.name) + ' as of ' + str(date_convert(db=time.y_m_d)) +
                 ' at ' + str(time_convert(db=time.h_m_s)) + '.\n\n')
        header = 'AMOUNT             DATE                  TIME    \n'
        undrln = '-------            ----------            --------\n'
        footer = '\n' + str(self.bal)

        if len(title) <= 49:
            self.details.l.config(width=49)
        else:
            self.details.l.config(width=len(title))

        report_list = [title, header, undrln]

        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")

        sql_cmd_charge = 'SELECT charge FROM finance WHERE patient_id=' + str(self.id) + ' ORDER BY date, time;'
        sql_cmd_date = 'SELECT date FROM finance WHERE patient_id=' + str(self.id) + ' ORDER BY date, time;'
        sql_cmd_time = 'SELECT time FROM finance WHERE patient_id=' + str(self.id) + ' ORDER BY date, time;'

        cursor_charge = connection.execute(sql_cmd_charge).fetchall()
        cursor_date = connection.execute(sql_cmd_date).fetchall()
        cursor_time = connection.execute(sql_cmd_time).fetchall()

        max_line = len(cursor_charge)
        cur_line = 0

        while cur_line < max_line:
            charge = cursor_charge[cur_line][0]
            date = cursor_date[cur_line][0]
            time = cursor_time[cur_line][0]
            report_list.append(self.assemble_line(charge, date, time))
            cur_line += 1

        report_list.append(footer)

        report = ""

        for line in report_list:
            report += line

        self.details.enable()
        self.details.insert(report)
        self.details.disable()

    def assemble_line(self, charge, date_db, time_db):

        cg = self.align_charge(charge)
        date = date_convert(db=date_db)
        time = time_convert(db=time_db)

        line = str(cg) + '            ' + str(date) + '            ' + str(time) + '\n'

        return line

    def align_charge(self, charge):
        cg = len(str(charge))
        if cg == 1:
            return '      ' + str(charge)
        elif cg == 2:
            return '     ' + str(charge)
        elif cg == 3:
            return '    ' + str(charge)
        elif cg == 4:
            return '   ' + str(charge)
        elif cg == 5:
            return '  ' + str(charge)
        elif cg == 6:
            return ' ' + str(charge)
        else:
            return str(charge)
