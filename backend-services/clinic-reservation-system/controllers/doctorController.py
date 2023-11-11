from services.doctorServices import *


def doctorIndex():
    return {
        'User Type': 'Doctor',
        'Health': 'App is Healthy',
        'Port': '5000',
        'Root': '/clinic'
    }


def createDoctorSlots():
    return createSlots()


def updateDoctorSlots():
    return updateSlots()


def cancelDoctorSlots():
    return cancelSlots()


def viewDoctorSlots():
    return viewSlots()


def getNames():
    return getDoctorNames()



