from root_file import *
from Functions.tk_objects import *

# GLOBAL CODE FOR BOTH WINDOWS
def back_btn():
    new_session.destroy()

# CODE FOR NEW SESSION WINDOW 1
new_session = Toplevel(root)
new_session.title('New Patient Session')
new_session.geometry('600x600')

part1 = Frame(new_session)

ins1 = Lbl(part1, 'Select patient and click next.')
ins2 = Lbl(part1, 'To add a new patient, go back and open Patient Manager.')

pat_list = List(part1, SINGLE)

# INSERT CODE TO ALLOW PYTHON TO PULL PATIENTS FROM .db FILE.
# ENSURE TO UTILIZE METHODS FOR RESETTING THE LIST UPON UPDATE.
# DUMMY NAMES ARE CURRENTLY INSERTED TO TEST FUNCTIONALITY.

# START DUMMY NAME CODE
pat_list.insert('John Doe')
pat_list.insert('Jane Doe')
pat_list.insert('Ryan Baxter')
pat_list.insert('Sarah Young')
# END DUMMY NAME CODE

def next_btn():
    name = pat_list.get_choice()
    if name is not NONE:
        # Launch new window.
        new_session.destroy()
    else:
        pop = Dialog(new_session, 'Error', 'Please select a patient to continue.')
        new_session.wait_window(pop)

back = Btn(part1, 'Back', back_btn)
nxt = Btn(part1, 'Next', next_btn)

def launch_new_session():
    part1.grid(row=0, column=0)
    ins1.l.grid(row=0, column=1)
    pat_list.l.grid(row=1, column=1)
    ins2.l.grid(row=2, column=1)
    back.b.grid(row=3, column=0)
    nxt.b.grid(row=3, column=2)
    mainloop()

# CODE FOR NEW SESSION WINDOW 2
part2 = Frame(new_session)

ins3 = Lbl(part2, 'Type session notes below. Then click Submit.')

notes = LargeTxtBox(part2)

cncl = Btn(part2, 'Cancel', back_btn)
sbmt = Btn(part2, 'Submit', back_btn) # Create "submit" fxn when database is set up.

def launch_notes_window():
    part2.grid(row=0, column=0)
    ins3.l.grid(row=0, column=1)
    notes.l.grid(row=1, column=1)
    cncl.b.grid(row=2, column=0)
    sbmt.b.grid(row=2, column=2)
    mainloop()






