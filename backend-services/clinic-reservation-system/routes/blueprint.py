from flask import Blueprint
from controllers.authController import *
from controllers.doctorController import *
from controllers.patientController import *

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/doctor', methods=['GET'])(doctorIndex)
blueprint.route('/patient', methods=['GET'])(patientIndex)
# 7 api features
blueprint.route('/signin/doctor', methods=['POST'])(doctorSignIn)
blueprint.route('/signup/doctor', methods=['POST'])(doctorSignUp)
blueprint.route('/signin/patient', methods=['POST'])(patientSignIn)
blueprint.route('/signup/patient', methods=['POST'])(patientSignUp)
blueprint.route('/create/doctorSlot', methods=['POST'])(createDoctorSlots)
blueprint.route('/view/doctorSlot', methods=['GET'])(viewDoctorSlots)
blueprint.route('/update/doctorSlot', methods=['PUT'])(updateDoctorSlots)
blueprint.route('/cancel/doctorSlot', methods=['DELETE'])(cancelDoctorSlots)
blueprint.route('/create/patientAppointment', methods=['POST'])(createPatientAppointment)
blueprint.route('/view/AvailableSlots/<string:doctorName>', methods=['GET'])(viewDoctorSlot)
blueprint.route('/view/patientAppointment', methods=['GET'])(viewPatientAppointment)
blueprint.route('/update/patientAppointment', methods=['PUT'])(updatePatientAppointment)
blueprint.route('/cancel/patientAppointment', methods=['DELETE'])(cancelPatientAppointment)

blueprint.errorhandler(404)(showMessage)

