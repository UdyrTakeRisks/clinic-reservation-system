import json
from services.patientServices import *


def patientIndex():
    return {
        'User Type': 'Patient',
        'Health': 'App is Healthy',
        'Port': '5000',
        'Root': '/clinic'
    }


def createPatientAppointment():
    return createAppointment()


def updatePatientAppointment():
    return updateAppointment()


def cancelPatientAppointment():
    return cancelAppointment()


def viewPatientAppointment():
    return viewAppointment()





