from root_file import *
from Functions.tk_objects import *
from new_session import launch_new_session

def b_test():
    print "Button Success"

def close_program():
    root.destroy()

main_menu = Toplevel(root)
main_menu.title('Main Menu')
main_menu.geometry('300x500')

pad_val = 5

title = Lbl(main_menu, 'Psychologist Database')

start = Btn(main_menu, 'Start New Session', launch_new_session)
appointment = Btn(main_menu, 'Appointment Calendar', b_test)
finance = Btn(main_menu, 'Patient Finance', b_test)
manage = Btn(main_menu, 'Patient Manager', b_test)
settings = Btn(main_menu, 'Settings', b_test)
exitButton = Btn(main_menu, 'Exit', close_program)

def launch_main_menu():
    title.l.pack()
    start.b.pack(pady=pad_val)
    appointment.b.pack(pady=pad_val)
    finance.b.pack(pady=pad_val)
    manage.b.pack(pady=pad_val)
    settings.b.pack(anchor=SE, side=LEFT)
    exitButton.b.pack(anchor=SW, side=RIGHT)
    mainloop()

