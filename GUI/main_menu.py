from tk_objects import *

def click_test():
    print "Click Success"

def close_program():
    root.destroy()

pad_val = 5

root = Tk()
root.title('Psychologist Database')
root.geometry('300x500')

title = Label(root)
title['text'] = 'Psychologist Database'
# title.pack()

start = Button(root)
start['text'] = 'Start New Session'
start['command'] = click_test
# start.pack(pady=pad_val)

appointment = Button(root)
appointment['text'] = 'Appointment Calendar'
appointment['command'] = click_test
# appointment.pack(pady=pad_val)

finance = Button(root)
finance['text'] = 'Patient Finances'
finance['command'] = click_test
# finance.pack(pady=pad_val)

manage = Button(root)
manage['text'] = 'Manage Patients'
manage['command'] = click_test
# manage.pack(pady=pad_val)

settings = Button(root)
settings['text'] = 'Settings'
settings['command'] = click_test
# settings.pack(anchor=SW)

exitButton = Button(root)
exitButton['text'] = 'Exit'
exitButton['command'] = close_program
# exitButton.pack(anchor=SE)

def launch_main_menu():
    title.pack()
    start.pack(pady=pad_val)
    appointment.pack(pady=pad_val)
    finance.pack(pady=pad_val)
    manage.pack(pady=pad_val)
    settings.pack(anchor=SE, side=LEFT)
    exitButton.pack(anchor=SW, side=RIGHT)
    mainloop()

