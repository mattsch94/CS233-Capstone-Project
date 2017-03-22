from root_file import *
from functions.tk_objects import *

new_session = Toplevel(root)
new_session.title('New Patient Session')
new_session.geometry('600x600')

ins1 = Text(new_session, 'Select patient and click next.')

pat_list = List(new_session, SINGLE)

# INSERT CODE TO ALLOW PYTHON TO PULL PATIENTS FROM .db FILE.
# DUMMY NAMES ARE CURRENTLY INSERTED TO TEST FUNCTIONALITY.

# START DUMMY NAME CODE
pat_list.insert(END, 'John Doe')
pat_list.insert(END, 'Jane Doe')
pat_list.insert(END, 'Ryan Baxter')
pat_list.insert(END, 'Sarah Young')
# END DUMMY NAME CODE



