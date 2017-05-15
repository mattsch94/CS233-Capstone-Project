# import sqlite3
from pysqlcipher import dbapi2 as sqlite3
from GUI.root_file import *
import operator
import datetime

class Patient:  # Datatype used to store patient information.

    def __init__(self, id_number):
        self.connection = sqlite3.connect(db_address)
        self.connection.executescript("pragma key='x41gq'")
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
            # return str(self.fname) + " " + str(self.lname) # First Last
            return str(self.lname) + ', ' + str(self.fname)  # Last, First
        else:
            parts = full.split()
            self.fname = str(parts[1])
            self.lname = str(parts[0])[0:'end-1']

class Patient_List:  # Object that holds multiple patients.

    def __init__(self):

        connection = sqlite3.connect(db_address)
        connection.executescript("pragma key='x41gq'")
        sql_cmd = 'SELECT patient_id FROM patients ORDER BY lname;'
        cursor = connection.execute(sql_cmd).fetchall()
        id_list = []
        self.pList = []

        for item in cursor:
            id_list.append(item[0])

        for cur_id in id_list:
            if self.confirm_id(cur_id):
                patient = Patient(cur_id)
                if patient.new == FALSE:
                    self.pList.append(patient)

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
        connection.executescript("pragma key='x41gq'")
        sql_stmt = "SELECT * FROM patients WHERE patient_id=" + str(identification_no)
        cursor = connection.execute(sql_stmt).fetchall()
        obtain = cursor
        connection.close()
        if obtain == []: return FALSE
        else: return TRUE

def max_patient_id():  # Determines what the largest patient ID is.
    connection = sqlite3.connect(db_address)
    self.connection.executescript("pragma key='x41gq'")
    sql_stmt = "SELECT MAX(patient_id) FROM patients;"
    cursor = connection.execute(sql_stmt).fetchone()
    obtain = cursor
    connection.close()
    if obtain[0] == None:
        return 0
    else:
        return obtain[0]

def date_convert(proper=NONE, db=NONE):  # Converts dates from proper convention to db-integer convention.
    if proper is not NONE and db is NONE:
        mm = str(proper[0:2])
        dd = str(proper[3:5])
        yyyy = str(proper[6:10])
        final = yyyy + mm + dd
        return final
    if proper is NONE and db is not NONE:
        yyyy = str(db[0:4])
        mm = str(db[4:6])
        dd = str(db[6:8])
        final = mm + '/' + dd + '/' + yyyy
        return final

def time_convert(proper=NONE, db=NONE):  # Converts time from proper convention to db-integer convention.
    if proper is not NONE and db is NONE:
        hh = str(proper[0:2])
        mm = str(proper[3:5])
        ss = str(proper[6:8])
        final = hh + mm + ss
        return final
    if proper is NONE and db is not NONE:
        hh = str(db[0:2])
        mm = str(db[2:4])
        ss = str(db[4:6])
        final = hh + ':' + mm + ':' + ss
        return final

class Time_Stamp: # Creates an object that stores date and time it was created. Values accessed via public variables.
                  # The values are stored in the object in "db-integer" convention.

    def __init__(self):

        i = datetime.datetime.now()
        year = i.year
        month = i.month
        day = i.day
        hh = i.hour
        mm = i.minute
        ss = i.second

        year_s = str(year)

        if month < 10:
            month_s = '0' + str(month)
        else:
            month_s = str(month)

        if day < 10:
            day_s = '0' + str(day)
        else:
            day_s = str(day)

        self.y_m_d = year_s + month_s + day_s   # Public variable accessed for date.

        if hh == 0:
            hour_s = '00'
        elif hh < 10:
            hour_s = '0' + str(hh)
        else:
            hour_s = str(hh)

        if mm == 0:
            min_s = '00'
        elif mm < 10:
            min_s = '0' + str(mm)
        else:
            min_s = str(mm)

        if ss == 0:
            sec_s = '00'
        elif ss < 10:
            sec_s = '0' + str(ss)
        else:
            sec_s = str(ss)

        self.h_m_s = hour_s + min_s + sec_s   # Public variable accessed for time.

    def reset(self):   # Resets the object. Updates the date and time to when reset is called.
        self.__init__()
