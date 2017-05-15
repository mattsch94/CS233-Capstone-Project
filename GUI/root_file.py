from Functions.tk_objects import *
# import sqlite3
from pysqlcipher import dbapi2 as sqlite3

root = Tk()
root.title('Psychologist Database')
root.withdraw()

db_address = "/Users/matt/GitHub/CS233-Capstone-Project/encrypted.db"

debug_mode = True

# Special debug functions only operate if "debug" is set to TRUE. This way, they functions can remain embedded
# in the code, and be turned off when the program is not being debugged.
debug = TRUE
