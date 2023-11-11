import datetime
import traceback
import pymysql.cursors
from flask import jsonify
from flask import request
from services.helpers import *


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
                        # what if another patientID had an appointment with the same doctor in diff slot
                        # what we will do here ! ans/ is we can know from the Slots table
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
    try:
        Json = request.json
        doctorName = Json['doctor']
        SlotDate = Json['slotDate']
        SlotHour = Json['slotHour']
        newDoctorName = Json['newDoctor']
        newSlotDate = Json['newSlotDate']
        newSlotHour = Json['newSlotHour']
        patientID = getPatientID()
        if patientID is None:
            response = jsonify('You should log in first to update your Appointment')
            response.status_code = 200
            return response
        else:
            if doctorName and SlotDate and SlotHour and newDoctorName and newSlotDate and newSlotHour and patientID and request.method == 'PUT':
                # Convert slot date in JSON response to the same format as the request
                SlotDate = datetime.datetime.strptime(SlotDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                if not (checkAppointmentExistence(SlotDate, SlotHour)):
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    sqlQuery1 = "SELECT id FROM Doctor WHERE name= %s"
                    bindData1 = doctorName
                    cursor.execute(sqlQuery1, bindData1)
                    row1 = cursor.fetchone()
                    doctorID = row1["id"]
                    sqlQuery2 = "SELECT id FROM Doctor WHERE name= %s"
                    bindData2 = newDoctorName
                    cursor.execute(sqlQuery2, bindData2)
                    row2 = cursor.fetchone()
                    newDoctorID = row2["id"]
                    newSlotDate = datetime.datetime.strptime(newSlotDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                    if checkDoctorSlotExistence(newSlotDate, newSlotHour, newDoctorID):
                        sqlQuery3 = ("UPDATE Slots "
                                     "SET patientID =%s "
                                     "WHERE slotDate =%s AND slotHour =%s AND doctorID =%s")
                        bindData3 = (patientID, newSlotDate, newSlotHour, newDoctorID)
                        cursor.execute(sqlQuery3, bindData3)
                        sqlQuery4 = ("UPDATE Slots "
                                     "SET patientID = NULL "
                                     "WHERE slotDate =%s AND slotHour =%s AND doctorID =%s")
                        bindData4 = (SlotDate, SlotHour, doctorID)
                        cursor.execute(sqlQuery4, bindData4)
                        # if the same doctor it overwrites the field
                        sqlQuery5 = ("UPDATE Doctor "
                                     "SET patientID = %s "
                                     "WHERE id =%s")
                        bindData5 = (patientID, newDoctorID)
                        cursor.execute(sqlQuery5, bindData5)
                        sqlQuery6 = "SELECT COUNT(*) FROM Slots WHERE doctorID = %s AND patientID =%s"
                        bindData6 = (doctorID, patientID)
                        cursor.execute(sqlQuery6, bindData6)
                        numOfAppointments = cursor.fetchone()['COUNT(*)']
                        if numOfAppointments < 1:
                            sqlQuery7 = ("UPDATE Doctor "
                                         "SET patientID = NULL "
                                         "WHERE id= %s AND patientID= %s")
                            bindData7 = (doctorID, patientID)
                            cursor.execute(sqlQuery7, bindData7)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        response = jsonify('Appointment updated successfully')
                        response.status_code = 200
                        return response
                    else:
                        response = jsonify('Doctor or Slot is NOT found, view available slots')
                        response.status_code = 200
                        return response
                else:
                    response = jsonify('Appointment is not found, please create it first')
                    response.status_code = 200
                    return response
    except Exception as err:
        traceback.print_exc()
        print(err)


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
                for appointmentRow in appointmentRows:
                    SlotDate = str(appointmentRow["slotDate"])
                    SlotHour = str(appointmentRow["slotHour"])
                    if not (checkAppointmentExistence(SlotDate, SlotHour)):
                        response = jsonify(appointmentRows)
                        response.status_code = 200
                        return response
                response = jsonify('No Patient Appointments to show')
                response.status_code = 200
                return response
            return {'No Patient Exist'}
    except Exception as err:
        traceback.print_exc()
        print(err)


def viewAvailableDoctorSlots(doctorName):
    try:
        # Json = request.json
        # doctorName = Json['doctor']
        patientID = getPatientID()
        if patientID is None:
            response = jsonify('You should log in first to view Doctor Slots')
            response.status_code = 200
            return response
        else:
            if checkPatientExistence():
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery1 = "SELECT id FROM Doctor WHERE name = %s"
                bindData1 = doctorName
                cursor.execute(sqlQuery1, bindData1)
                row = cursor.fetchone()
                if row is None:
                    response = jsonify('Doctor is not found')
                    response.status_code = 200
                    return response
                else:
                    doctorID = row["id"]
                    sqlQuery2 = "SELECT slotDate, slotHour FROM Slots WHERE doctorID =%s AND patientID is NULL"
                    bindData2 = doctorID
                    cursor.execute(sqlQuery2, bindData2)
                    docSlotRows = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    for docSlotRow in docSlotRows:
                        SlotDate = str(docSlotRow["slotDate"])
                        SlotHour = str(docSlotRow["slotHour"])
                        if checkDoctorSlotExistence(SlotDate, SlotHour, doctorID):
                            response = jsonify(docSlotRows)
                            response.status_code = 200
                            return response
                response = jsonify('No Available Slots to show')
                response.status_code = 200
                return response

            return {'No Patient Exist'}
    except Exception as err:
        traceback.print_exc()
        print(err)
