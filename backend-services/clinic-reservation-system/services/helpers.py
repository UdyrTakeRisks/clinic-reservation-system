import pymysql.cursors
from config import mysql
from services.authService import doctor, checkDoctorExistence
from services.authService import patient, checkPatientExistence


# doctor helpers


def checkSlotExistence(SlotDate, SlotHour):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT slotDate, slotHour, doctorID FROM Slots"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for row in rows:
            if SlotDate == str(row["slotDate"]) and SlotHour == row["slotHour"] and getDoctorID() == row["doctorID"]:
                return False
        conn.close()
    except Exception as err:
        print(err)
    return True


def getDoctorID():
    try:
        if checkDoctorExistence():
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "SELECT id FROM Doctor WHERE name =%s AND password =%s"
            bindData = (doctor.getName(), doctor.getPassword())
            cursor.execute(sqlQuery, bindData)
            row = cursor.fetchone()
            doctorID = row["id"]
            conn.close()
            return doctorID
        return None
    except Exception as err:
        print(err)


# patient helpers


def getPatientID():
    try:
        if checkPatientExistence():
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "SELECT id FROM Patient WHERE name =%s AND password =%s"
            bindData = (patient.getName(), patient.getPassword())
            cursor.execute(sqlQuery, bindData)
            row = cursor.fetchone()
            patientID = row["id"]
            conn.close()
            return patientID
        return None
    except Exception as err:
        print(err)


def checkAppointmentExistence(SlotDate, SlotHour):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT slotDate, slotHour, patientID FROM Slots"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for row in rows:
            if SlotDate == str(row["slotDate"]) and SlotHour == row["slotHour"] and getPatientID() == row["patientID"]:
                return False
        conn.close()
    except Exception as err:
        print(err)
    return True


def checkDoctorSlotExistence(SlotDate, SlotHour, doctorID):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT slotDate, slotHour, doctorID FROM Slots"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for row in rows:
            if SlotDate == str(row["slotDate"]) and SlotHour == row["slotHour"] and doctorID == row["doctorID"]:
                return True
        conn.close()
    except Exception as err:
        print(err)
    return False
