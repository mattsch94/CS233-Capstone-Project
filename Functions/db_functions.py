import sqlite3
from GUI.root_file import *

class DB_Connection:

    def __init__(self):
        self.connection = sqlite3.connect(db_address)



class Patient:

    def __init__(self, id_number):
        self.connection = sqlite3.connect(db_address)
        self.id_num = id_number
        sql_stmt = "SELECT * FROM patients WHERE patient_id = " + str(id_number)
        self.cursor = self.connection.execute(sql_stmt).fetchall()

        if self.cursor == []:
            self.fname = NONE
            self.lname = NONE
            self.bday = NONE
            self.address = NONE
            self.phone = NONE
            self.new = TRUE
        else:
            temp_list = []
            for item in self.cursor[0]:
                temp_list.append(item)
            self.fname = temp_list[1]
            self.lname = temp_list[2]
            self.bday = temp_list[3]
            self.address = temp_list[4]
            self.phone = temp_list[5]
            self.new = FALSE

    def __del__(self):
        self.connection.close()

    def update(self):
        if self.new == FALSE:
            sql_stmt_del = "DELETE FROM patients WHERE patient_id=" + str(self.id_num)
            self.connection.execute(sql_stmt_del)
            self.connection.commit()

        st1 = "INSERT INTO patients VALUES ("
        st2 = ", "
        st3 = ");"
        sql_stmt = (st1 + str(self.id_num) + st2 + str(self.fname) + st2 + str(self.lname) + st2 +
                    str(self.bday) + st2 + str(self.address) + st2 + str(self.phone) + st3)
        self.connection.execute(sql_stmt)
        self.connection.commit()

    def full_name(self, full=NONE):
        if full == NONE:
            return str(self.fname) + " " + str(self.lname)
        else:
            parts = full.split()
            self.fname = str(parts[0])
            self.lname = str(parts[1])

doe = Patient(1)
print(doe.full_name())
print(doe.phone)
doe.__del__()
