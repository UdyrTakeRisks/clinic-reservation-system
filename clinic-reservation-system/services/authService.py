import pymysql.cursors
from config import mysql
from flask import jsonify
from flask import request

from models.Doctor import Doctor
from models.Patient import Patient

doctor = Doctor()
patient = Patient()


def doctorLogin():
    try:
        Json = request.json
        Name = Json['name']
        Password = Json['password']
        # set name and pass in Patient class when logged in
        doctor.setName(Name)
        doctor.setPassword(Password)
        if Name and Password and request.method == 'POST':
            if checkDoctorExistence():
                response = jsonify('Doctor logged in successfully')
                response.status_code = 200
                return response
            else:
                response = jsonify('Please Doctor Register First')
                response.status_code = 200
                return response
        else:
            return showMessage()
    except Exception as err:
        print(err)


def doctorRegister():
    try:
        if request.method == 'POST':
            Json = request.json
            Name = Json['name']
            Email = Json['email']
            Password = Json['password']
            if Name and Email and Password:
                if checkDoctorRegisteredBefore(Name, Password):
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    sqlQuery = "INSERT INTO Doctor(name, email, password) VALUES(%s, %s, %s)"
                    bindData = (Name, Email, Password)
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    response = jsonify({'message': 'Doctor Registered successfully'})
                    response.status_code = 200
                    return response
                else:
                    response = jsonify({'message': 'You already registered, Please log in'})
                    response.status_code = 200
                    return response
    except Exception as err:
        print(err)
        response = jsonify({'error': 'Error in Registering The Doctor'})
        response.status_code = 500
        return response


def patientLogin():
    try:
        Json = request.json
        Name = Json['name']
        Password = Json['password']
        if Name and Password and request.method == 'POST':
            # set name and pass in Patient class when logged in
            patient.setName(Name)
            patient.setPassword(Password)
            if checkPatientExistence():
                response = jsonify('Patient logged in successfully')
                response.status_code = 200
                return response
            else:
                response = jsonify('Please Patient Register First')
                response.status_code = 200
                return response
        else:
            return showMessage()
    except Exception as err:
        print(err)


def patientRegister():
    try:
        Json = request.json
        Name = Json['name']
        Email = Json['email']
        Password = Json['password']

        if Name and Email and Password and request.method == 'POST':
            if checkPatientRegisteredBefore(Name, Password):
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery = "INSERT INTO Patient(name, email, password) VALUES(%s, %s, %s)"
                bindData = (Name, Email, Password)
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                cursor.close()
                conn.close()
                response = jsonify('Patient Registered successfully')
                response.status_code = 200
                return response
            else:
                response = jsonify('You already registered, Please log in')
                response.status_code = 200
                return response
        else:
            return showMessage()
    except Exception as err:
        print(err)


def showMessage():
    message = {
        'status': 404,
        'Message': 'Record not found' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


def checkDoctorExistence():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT name, password FROM Doctor"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for row in rows:
            if doctor.getName() == row["name"] and doctor.getPassword() == row["password"]:
                return True
        conn.close()
    except Exception as err:
        print(err)
    return False


def checkPatientExistence():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT name, password FROM Patient"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for row in rows:
            if patient.getName() == row["name"] and patient.getPassword() == row["password"]:
                return True
        conn.close()
    except Exception as err:
        print(err)
    return False


def checkDoctorRegisteredBefore(Name, Password):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT name, password FROM Doctor"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for row in rows:
            if Name == row["name"] and Password == row["password"]:
                return False
        conn.close()
    except Exception as err:
        print(err)
    return True


def checkPatientRegisteredBefore(Name, Password):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT name, password FROM Patient"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for row in rows:
            if Name == row["name"] and Password == row["password"]:
                return False
        conn.close()
    except Exception as err:
        print(err)
    return True
