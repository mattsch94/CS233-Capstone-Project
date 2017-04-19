from Functions.tk_objects import *
from tkinter.messagebox import *
from Functions.db_functions import *
from main_menu import launch_main_menu

class Log_In_Window:  # Manages the log-in window that grants access to the rest of the program.

    def __init__(self):

        self.window = Toplevel(root)
        self.window.title('Log In')
        # self.window.geometry('300x150')
        self.user_text = Lbl(self.window, 'User ID:')
        self.password_text = Lbl(self.window, 'Password:')
        self.user_entry = TxtBox(self.window)
        self.password_entry = TxtBox(self.window)
        self.password_entry.password(TRUE)
        self.login = Btn(self.window, 'Log In', self.verify)
        self.exit = Btn(self.window, 'Exit', self.close)

        self.pad = 5

        self.user_verify = FALSE
        self.pass_verify = FALSE
        self.admin_verify = FALSE

    def launch(self):

        # The two lines below should be removed upon program completion.
        self.user_entry.insert('358679')
        self.password_entry.insert('laptop@10309')

        self.user_text.l.grid(row=0, column=0, pady=self.pad)
        self.user_entry.t.grid(row=0, column=1, pady=self.pad)
        self.password_text.l.grid(row=1, column=0, pady=self.pad)
        self.password_entry.t.grid(row=1, column=1, pady=self.pad)
        self.login.b.grid(row=2, column=0, pady=self.pad)
        self.exit.b.grid(row=2, column=1, pady=self.pad)
        mainloop()

    def login_error(self):
        showerror('Error', 'Invalid login credentials.')

    def close(self):
        root.destroy()

    def verify(self):

        username = self.user_entry.get_text()
        password = self.password_entry.get_text()

        if not str(username).isdigit():
            self.login_error()
            return

        connection = sqlite3.connect(db_address)
        users = connection.execute('SELECT user_id FROM users;').fetchall()

        for user in users:
            if str(user[0]) == str(username):
                self.user_verify = TRUE
                break

        if self.user_verify == FALSE:
            self.login_error()
            return

        sql_cmd_1 = "SELECT password FROM users WHERE user_id=" + str(username) + ";"
        pswd = connection.execute(sql_cmd_1).fetchone()
        if pswd[0] == password:
            self.pass_verify = TRUE
        else:
            self.login_error()
            return
        sql_cmd_2 = 'SELECT admin FROM users WHERE user_id=' + str(username) + ';'
        admin = connection.execute(sql_cmd_2).fetchone()

        if admin[0]:
            self.admin_verify = TRUE
        else:
            self.admin_verify = FALSE
        if self.user_verify and self.pass_verify:
            self.window.destroy()
            launch_main_menu(self.admin_verify, username)
            connection.close()
            return
        else:
            self.login_error()
            return

def start_program():  # Launches the log-in window.

    start = Log_In_Window()
    start.launch()

class User_Manager_Admin:  # Manages the user-manager accessable by admin users.

    def __init__(self, user_id):

        self.window = Toplevel(root)
        self.window.title('User Manager')
        # self.window.geometry('500x500')

        pad = 5

        self.user_disp = List(self.window)
        self.new = Btn(self.window, 'New User', self.new)
        self.edit = Btn(self.window, 'Edit User', self.edit)
        self.delete = Btn(self.window, 'Delete User', self.delete)
        self.refresh = Btn(self.window, 'Refresh List', self.refresh_list)
        self.close = Btn(self.window, 'Close Window', self.window.destroy)

        self.user_disp.l.grid(row=0, column=0, pady=pad)
        self.new.b.grid(row=1, column=0, pady=pad)
        self.edit.b.grid(row=2, column=0, pady=pad)
        self.delete.b.grid(row=3, column=0, pady=pad)
        self.refresh.b.grid(row=4, column=0, pady=pad)
        self.close.b.grid(row=5, column=0, pady=pad)

        self.active_id = user_id

        self.refresh_list()

    def refresh_list(self):
        self.user_disp.delete_all()
        connection = sqlite3.connect(db_address)
        cursor = connection.execute('SELECT user_id FROM users;').fetchall()
        for user in cursor:
            self.user_disp.insert(str(user[0]))
        connection.close()
        self.new.state(TRUE)
        self.edit.state(TRUE)
        self.delete.state(TRUE)

    def new(self):
        User()
        self.disable_before_refresh()

    def edit(self):
        if self.user_disp.get_choice():
            user_id = self.user_disp.get_choice()
        else:
            showerror('Error', 'Please select a User ID to continue.')
            return

        connection = sqlite3.connect(db_address)
        sql_cmd_pass = 'SELECT password FROM users WHERE user_id=' + str(user_id) + ';'
        sql_cmd_admin = 'SELECT admin FROM users WHERE user_id=' + str(user_id) + ';'
        cursor_pass = connection.execute(sql_cmd_pass).fetchone()[0]
        cursor_admin = connection.execute(sql_cmd_admin).fetchone()[0]

        if (user_id == self.active_id):
            not_me = False
        else:
            not_me = True

        User(user_id, cursor_pass, cursor_admin, not_me)
        self.disable_before_refresh()
        connection.close()

    def delete(self):
        if self.user_disp.get_choice():
            user_id = self.user_disp.get_choice()
        else:
            showerror('Error', 'Please select a User ID to continue.')
            return

        if user_id == self.active_id:
            showerror('Error', 'The active profile cannot be deleted.')
            return

        confirm_msg = 'Are you sure you want to delete User ID ' + str(user_id) + '?'
        if askyesno('Confirm', confirm_msg):
            connection = sqlite3.connect(db_address)
            sql_cmd = 'DELETE FROM users WHERE user_id=' + str(user_id) + ';'
            connection.execute(sql_cmd)
            connection.commit()
            connection.close()
            self.disable_before_refresh()

    def disable_before_refresh(self):
        self.new.state(FALSE)
        self.edit.state(FALSE)
        self.delete.state(FALSE)

def User_Manager_Std(user):  # Allows non-admin users to change their password.
    connection = sqlite3.connect(db_address)
    sql_cmd = 'SELECT password FROM users WHERE user_id=' + str(user) + ';'
    pw = connection.execute(sql_cmd).fetchone()[0]

    User(user, pw, False, False)

    connection.close()

class User:  # Manages the editor window used to create/change user information.

    def __init__(self, user=None, pw=None, acct=None, curr_admin=True):

        self.window = Toplevel(root)
        self.window.title('User Info')
        # self.window.geometry('500x500')

        self.user_text = Lbl(self.window, '        User ID:')
        self.pswd_text = Lbl(self.window, '       Password:')
        self.vf_pswd_text = Lbl(self.window, 'Verify Password:')
        self.type_text = Lbl(self.window, '      User Type:')

        self.user_entry = TxtBox(self.window)
        self.pswd_entry = TxtBox(self.window)
        self.vf_pswd_entry = TxtBox(self.window)

        self.submit = Btn(self.window, 'Submit', self.update)
        self.cancel = Btn(self.window, 'Cancel', self.close)

        self.pswd_entry.password(True)
        self.vf_pswd_entry.password(True)

        self.curr_admin = curr_admin

        self.admin = None

        self.admin_got = None
        self.a_true = '<Admin>'
        self.a_false = '<Limited>'
        self.type_admin = Btn(self.window, 'Admin', self.radio_true)
        self.type_normal = Btn(self.window, 'Limited', self.radio_false)
        self.type_display = Lbl(self.window, '<User Type>')

        self.edit_bool = False
        self.old_user = 0

        if user and pw:
            self.user_entry.insert(user)
            self.pswd_entry.insert(pw)
            self.vf_pswd_entry.insert(pw)
            self.admin = acct
            if self.admin:
                self.type_display.text(self.a_true)
            else:
                self.type_display.text(self.a_false)
            self.old_user = user
            self.edit_bool = True

        if not self.curr_admin:
            self.user_entry.disable()
            self.type_admin.state(FALSE)
            self.type_normal.state(FALSE)

        self.user_text.l.grid(row=0, column=0)
        self.user_entry.t.grid(row=0, column=1, columnspan=2)
        self.pswd_text.l.grid(row=1, column=0)
        self.pswd_entry.t.grid(row=1, column=1, columnspan=2)
        self.vf_pswd_text.l.grid(row=2, column=0)
        self.vf_pswd_entry.t.grid(row=2, column=1, columnspan=2)
        self.type_text.l.grid(row=3, column=0)
        self.type_admin.b.grid(row=3, column=1)
        self.type_normal.b.grid(row=3, column=2)
        self.type_display.l.grid(row=4, column=1)
        self.submit.b.grid(row=4, column=0)
        self.cancel.b.grid(row=4, column=2)

    def user_input_error(self):
        error_msg = ('Please enter a User ID that meets the following standards:\n' +
                     '-Field cannot be blank.\n-ID must be made up of only numbers.\n' +
                     '-ID cannot be more than 10 digits.\n-Minimum number for an ID is 1.\n' +
                     '-ID numbers must be unique.')
        showerror('Error', error_msg)

    def radio_true(self):
        self.admin = True
        self.type_display.text(self.a_true)

    def radio_false(self):
        self.admin = False
        self.type_display.text(self.a_false)

    def update(self):

        if not self.curr_admin:
            self.user_entry.enable()
            user_type = self.user_entry.get_text()
            self.user_entry.disable()
        else:
            user_type = self.user_entry.get_text()
        pass_type = str(self.pswd_entry.get_text())
        vf_pass_type = str(self.vf_pswd_entry.get_text())
        # self.admin
        # self.edit_bool

        if user_type == self.old_user:
            exclude = True
        else:
            exclude = False

        print user_type, self.old_user, exclude

        connection = sqlite3.connect(db_address)

        # User ID Verification
        cursor = connection.execute('SELECT user_id FROM users;').fetchall()
        user_list = []
        if exclude:
            for user in cursor:
                if int(user[0]) != int(self.old_user):
                    user_list.append(user[0])
        else:
            for user in cursor:
                user_list.append(user[0])
        '''
        if (not user_type or not str(user_type).isdigit() or user_type > 9999999999 or user_type < 1
            or user_type in user_list):
        '''
        if not user_type:
            self.user_input_error()
            print 'Blank Field'
            return
        elif not str(user_type).isdigit():
            self.user_input_error()
            print 'Not a Number'
            return
        elif int(user_type) > 9999999999:
            self.user_input_error()
            print 'More than 10 Digits'
            return
        elif int(user_type) < 1:
            self.user_input_error()
            print 'Less than 1'
            return
        elif int(user_type) in user_list:
            self.user_input_error()
            print 'Repeat ID Number'
            return
        else:
            print 'ID Verified'

        # Password Verification
        lowerAlphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        upperAlphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        specialChar = ['!', '@', '#', '$', '%', '^', '&', '*', '?']
        numberChar = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        lowerBool = False
        upperBool = False
        specialBool = False
        numberBool = False

        for char in pass_type:
            if char in lowerAlphabet:
                lowerBool = True
            if char in upperAlphabet:
                upperBool = True
            if char in specialChar:
                specialBool = True
            if char in numberChar:
                numberBool = True
            if lowerBool and upperBool and specialBool and numberBool:
                break

        if not lowerBool and not upperBool and not specialBool and not numberBool:
            error_msg = ('Please use a password that contains at least one of the following:\n' +
                         '-Uppercase Letter\n-Lowercase Letter\n-Number\n' +
                         '-One of these special characters:\n'
                         '   ! @ # $ % ^ & * ?')
            showerror('Error', error_msg)
            return

        # Vf_Password Verification
        if pass_type != vf_pass_type:
            showerror('Error', 'Both password fields must match.')
            return

        # Admin Verification
        print self.admin
        if self.admin == None:
            showerror('Error', 'A user type must be selected.')
            return

        # Database Deletion and Insertion
        if self.edit_bool:
            sql_cmd = 'DELETE FROM users WHERE user_id=' + str(self.old_user)
            connection.execute(sql_cmd)
            connection.commit()

        print self.admin
        if self.admin == True:
            admin_num = 1
        else:
            admin_num = 0

        sql_cmd = 'INSERT INTO users VALUES (' + str(user_type) + ', "' + str(pass_type) +'", ' + str(admin_num) + ');'
        connection.execute(sql_cmd)
        connection.commit()
        showinfo('Success', 'User information updated successfully.')
        self.window.destroy()

    def close(self):
        if askyesno('Confirm', 'Are you sure you want to cancel?'):
            self.window.destroy()
