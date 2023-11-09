import datetime
import traceback
import pymysql.cursors
from config import mysql
from flask import jsonify
from flask import request
from services.authService import patient, checkPatientExistence


def createAppointment():
    try:
        Json = request.json
        DoctorName = Json['doctor']
        SlotDate = Json['slotDate']
        SlotHour = Json['slotHour']
        patientID = getPatientID()
        if patientID is None:
            response = jsonify('You should log in first to create your appointments')
            response.status_code = 200
            return response
        else:
            if SlotDate and SlotHour and patientID and request.method == 'POST':
                # Convert slot date in JSON response to the same format as the request
                SlotDate = datetime.datetime.strptime(SlotDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                if checkAppointmentExistence(SlotDate, SlotHour):
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)

                    sqlQuery1 = "SELECT id FROM Doctor WHERE name= %s"
                    bindData1 = DoctorName
                    cursor.execute(sqlQuery1, bindData1)
                    row = cursor.fetchone()
                    doctorID = row["id"]
                    # check if doctor id != id so doctor is not found
                    if checkDoctorSlotExistence(SlotDate, SlotHour, doctorID):
                        sqlQuery2 = "UPDATE Doctor SET patientID= %s WHERE id= %s"
                        bindData2 = (patientID, doctorID)
                        cursor.execute(sqlQuery2, bindData2)

                        sqlQuery3 = "UPDATE Slots SET patientID= %s WHERE slotDate= %s AND slotHour= %s AND doctorID= %s"
                        bindData3 = (patientID, SlotDate, SlotHour, doctorID)
                        cursor.execute(sqlQuery3, bindData3)

                        conn.commit()
                        cursor.close()
                        conn.close()
                        response = jsonify('Appointment added successfully')
                        response.status_code = 200
                        return response
                    else:
                        response = jsonify('Slot is not found')
                        response.status_code = 200
                        return response
                else:
                    response = jsonify('Appointment is already found or Doctor is not found')
                    response.status_code = 200
                    return response
    except Exception as err:
        traceback.print_exc()
        print(err)


def updateAppointment():
    return {}


def cancelAppointment():
    try:
        patientID = getPatientID()
        if patientID is None:
            response = jsonify('You should log in first to cancel your Appointment')
            response.status_code = 200
            return response
        else:
            Json = request.json
            DoctorName = Json['doctor']
            SlotDate = Json['slotDate']
            SlotHour = Json['slotHour']
            # Convert slot date in JSON response to the same format as the request
            SlotDate = datetime.datetime.strptime(SlotDate, "%Y-%m-%d").strftime("%Y-%m-%d")
            if checkPatientExistence() and not (checkAppointmentExistence(SlotDate, SlotHour)):
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)

                sqlQuery1 = "UPDATE Slots SET patientID = NULL WHERE slotDate= %s AND slotHour= %s AND patientID = %s"
                bindData1 = (SlotDate, SlotHour, patientID)
                cursor.execute(sqlQuery1, bindData1)

                sqlQuery2 = "SELECT COUNT(*) FROM Slots WHERE doctorID = (SELECT id FROM Doctor WHERE name =%s) AND patientID =%s"
                bindData2 = (DoctorName, patientID)
                cursor.execute(sqlQuery2, bindData2)
                numOfAppointments = cursor.fetchone()['COUNT(*)']

                if numOfAppointments < 1:
                    sqlQuery3 = "UPDATE Doctor SET patientID = NULL WHERE name= %s AND patientID= %s"
                    bindData3 = (DoctorName, patientID)
                    cursor.execute(sqlQuery3, bindData3)
                conn.commit()
                cursor.close()
                conn.close()
                response = jsonify('Appointment is cancelled successfully')
                response.status_code = 200
                return response
            else:
                response = jsonify('No Appointment Found to cancel')
                response.status_code = 200
                return response
    except Exception as err:
        print(err)


def viewAppointment():
    try:
        patientID = getPatientID()
        if patientID is None:
            response = jsonify('You should log in first to view your Appointments')
            response.status_code = 200
            return response
        else:
            if checkPatientExistence():
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery = ("SELECT D.name, S.slotDate, S.slotHour "
                            "FROM Slots AS S "
                            "JOIN Doctor AS D "
                            "ON S.doctorID = D.id "
                            "WHERE S.patientID = %s")
                bindData = patientID
                cursor.execute(sqlQuery, bindData)
                appointmentRows = cursor.fetchall()
                cursor.close()
                conn.close()
                # if not (checkAppointmentExistence(SlotDate, SlotHour)):
                response = jsonify(appointmentRows)
                response.status_code = 200
                return response
                # else:
                #     response = jsonify('No Patient Appointments to show')
                #     response.status_code = 200
                #     return response

            return {'No Patient Exist'}
    except Exception as err:
        traceback.print_exc()
        print(err)


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
