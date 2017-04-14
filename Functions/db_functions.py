import sqlite3
from GUI.root_file import *

class Patient:

    def __init__(self, id_number):
        self.connection = sqlite3.connect(db_address)
        self.id_num = id_number
        sql_stmt = "SELECT * FROM patients WHERE patient_id=" + str(id_number)
        self.cursor = self.connection.execute(sql_stmt).fetchall()

        if self.cursor == []:  # Changed .cursor[0] to .cursor, if error occurs, may be caused here.
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

        sql_stmt = ('INSERT INTO patients VALUES (' +
                    str(self.id_num) + ', ' +
                    '"' + str(self.fname) + '", ' +
                    '"' + str(self.lname) + '", ' +
                    '"' + str(self.bday) + '", ' +
                    '"' + str(self.address) + '", ' +
                    '"' + str(self.phone) + '");')

        self.connection.execute(sql_stmt)
        self.connection.commit()

    def full_name(self, full=NONE):
        if full == NONE:
            return str(self.fname) + " " + str(self.lname)
        else:
            parts = full.split()
            self.fname = str(parts[0])
            self.lname = str(parts[1])

class Patient_List:

    def __init__(self):
        max_id = max_patient_id()
        cur_id = 1
        self.pList = []

        while cur_id < max_id+1:
            if self.confirm_id(cur_id):
                patient = Patient(cur_id)
                if patient.new == FALSE:
                    self.pList.append(patient)
            cur_id += 1

    def name(self, patient_id):
        for patient in self.pList:
            if patient.id_num == patient_id:
                return patient.full_name()
        return NONE

    def id(self, patient_full_name):

        for patient in self.pList:
            if patient.full_name() == patient_full_name:
                return patient.id_num
        return NONE

    def confirm_id(self, identification_no):
        connection = sqlite3.connect(db_address)
        sql_stmt = "SELECT * FROM patients WHERE patient_id=" + str(identification_no)
        cursor = connection.execute(sql_stmt).fetchall()
        obtain = cursor
        connection.close()
        if obtain == []: return FALSE
        else: return TRUE

def max_patient_id():
    connection = sqlite3.connect(db_address)
    sql_stmt = "SELECT MAX(patient_id) FROM patients;"
    cursor = connection.execute(sql_stmt).fetchone()
    obtain = cursor
    connection.close()
    return obtain[0]

'''
p = Patient_List()
print p.name(4)
print p.id(p.name(4))
'''