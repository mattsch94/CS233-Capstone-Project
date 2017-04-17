from root_file import *
from Functions.tk_objects import *
from new_session import launch_new_session
from patient_manager import launch_manager
from Functions.db_functions import *
import users

class Main_Menu:

    def __init__(self, admin, id_num):
        self.main_menu = Toplevel(root)
        self.main_menu.title('Main Menu')
        # self.main_menu.geometry('350x250')

        self.title = Lbl(self.main_menu, 'Psychologist Database')

        self.pad_val = 5

        self.is_user_admin = admin
        self.user_id = id_num

        self.start = Btn(self.main_menu, 'Start New Session', launch_new_session)
        self.appointment = Btn(self.main_menu, 'Appointment Calendar', self.b_test)
        self.finance = Btn(self.main_menu, 'Patient Finance', self.b_test)
        self.manage = Btn(self.main_menu, 'Patient Manager', self.launch_manage)
        self.users = Btn(self.main_menu, 'User Admin', None)
        self.logout = Btn(self.main_menu, 'Log Out', self.logout)
        self.exitButton = Btn(self.main_menu, 'Exit', self.close_program)

        if self.is_user_admin:
            self.users.command(self.launch_admin_user_mgr)
        else:
            self.users.command(self.launch_std_user_mgr)

    def b_test(self):
        print "Button Success"

    def close_program(self):
        root.destroy()

    def launch_manage(self):
        launch_manager(self.is_user_admin)

    def launch_admin_user_mgr(self):
        users.User_Manager_Admin(self.user_id)

    def launch_std_user_mgr(self):
        users.User_Manager_Std(self.user_id)

    def launch(self):
        self.title.l.grid(row=0, column=1, columnspan=1, pady=self.pad_val)

        if self.is_user_admin:
            self.start.state(TRUE)
        else:
            self.start.state(FALSE)

        self.start.b.grid(row=1, column=1, pady=self.pad_val)
        self.appointment.b.grid(row=2, column=1, pady=self.pad_val)
        self.finance.b.grid(row=3, column=1, pady=self.pad_val)
        self.manage.b.grid(row=4, column=1, pady=self.pad_val)
        self.users.b.grid(row=5, column=0, pady=self.pad_val)
        self.logout.b.grid(row=5, column=1, pady=self.pad_val)
        self.exitButton.b.grid(row=5, column=2, pady=self.pad_val)
        mainloop()

    def logout(self):
        self.main_menu.destroy()
        users.start_program()

def launch_main_menu(admin, id_num):

    menu = Main_Menu(admin, id_num)
    menu.launch()



