from Functions.tk_objects import *
# import sqlite3
from pysqlcipher import dbapi2 as sqlite3

class Pragma:

    def __init__(self):

        self.key = None
        self.query = None

    def update_key(self, new_key):

        self.key = str(new_key)
        self.query = "pragma key='" + self.key + "';"

root = Tk()
root.title('Psychologist Database')
root.withdraw()

db_address = "/Users/matt/GitHub/CS233-Capstone-Project/encrypted.db"
pragma = Pragma()
