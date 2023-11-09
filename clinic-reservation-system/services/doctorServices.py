import datetime
import pymysql.cursors
from config import mysql
from flask import jsonify
from flask import request
from services.authService import doctor, checkDoctorExistence


def createSlots():
    try:
        Json = request.json
        SlotDate = Json['slotDate']
        SlotHour = Json['slotHour']
        docID = getDoctorID()
        if docID is None:
            response = jsonify('You should log in first to add your slots')
            response.status_code = 200
            return response
        else:
            if SlotDate and SlotHour and docID and request.method == 'POST':
                # Convert slot date in JSON response to the same format as the request
                SlotDate = datetime.datetime.strptime(SlotDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                if checkSlotExistence(SlotDate, SlotHour):
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    sqlQuery = "INSERT INTO Slots(slotDate, slotHour, doctorID) VALUES(%s, %s, %s)"
                    bindData = (SlotDate, SlotHour, docID)
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    response = jsonify('Slot added successfully')
                    response.status_code = 200
                    return response
                else:
                    response = jsonify('Slot is already found')
                    response.status_code = 200
                    return response
    except Exception as err:
        print(err)


def updateSlots():
    return {}


def cancelSlots():
    try:
        docID = getDoctorID()
        if docID is None:
            response = jsonify('You should log in first to cancel your slot')
            response.status_code = 200
            return response
        else:
            Json = request.json
            SlotDate = Json['slotDate']
            SlotHour = Json['slotHour']
            # Convert slot date in JSON response to the same format as the request
            SlotDate = datetime.datetime.strptime(SlotDate, "%Y-%m-%d").strftime("%Y-%m-%d")
            if checkDoctorExistence() and not (checkSlotExistence(SlotDate, SlotHour)):
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery = "DELETE FROM Slots WHERE slotDate= %s AND slotHour= %s AND doctorID = %s"
                bindData = (SlotDate, SlotHour, docID)
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                cursor.close()
                conn.close()
                response = jsonify('Slot is deleted successfully')
                response.status_code = 200
                return response
            else:
                response = jsonify('No Slot Found to delete')
                response.status_code = 200
                return response
    except Exception as err:
        print(err)


def viewSlots():
    try:
        docID = getDoctorID()
        if docID is None:
            response = jsonify('You should log in first to view your slots')
            response.status_code = 200
            return response
        else:
            if checkDoctorExistence():
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery = "SELECT slotDate, slotHour FROM Slots WHERE doctorID =%s"
                bindData = docID
                cursor.execute(sqlQuery, bindData)
                slotRows = cursor.fetchall()
                response = jsonify(slotRows)
                response.status_code = 200
                cursor.close()
                conn.close()
                return response
            return {'No Slots to show'}
    except Exception as err:
        print(err)


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
