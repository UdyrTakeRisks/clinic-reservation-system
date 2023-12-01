// patient-page.component.ts

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DatePipe } from '@angular/common';


@Component({
  selector: 'app-patient-page',
  templateUrl: './patient-page.component.html',
  styleUrls: ['./patient-page.component.css'],
  providers: [DatePipe]
})
export class PatientPageComponent implements OnInit {
  welcomeMessage = 'Welcome, Patient';
  availableSlots: any[] = [];
  doctorNames: string[] = [];
  selectedDoctor: string = '';
  selectedSlot: any = '';
  doctorName: string = '';

  patientAppointments: any[] = [];
  isEditPopupVisible: boolean = false;
  selectedEditDoctor: string = '';
  selectedEditSlot: any = '';

  doctor: string = '';
  slotDate: string = '';
  slotHour: string = '';

  newDoctor: string = '';
  newSlotDate: string = '';
  newSlotHour: string = '';

  constructor(private http: HttpClient, private datePipe: DatePipe) { }

  // ----------------------------------------------------------------
  // formatDate and formatTime functions
  private formatDate(date: string): string {
    try {
      const parsedDate = new Date(date);

      // Check if the parsedDate is a valid date
      if (!isNaN(parsedDate.getTime())) {
        const formattedDate = this.datePipe.transform(parsedDate, 'yyyy-MM-dd');
        return formattedDate || ''; // Return an empty string if the format is invalid
      } else {
        console.error('Invalid date:', date);
        return ''; // Return an empty string for invalid dates
      }
    } catch (error) {
      console.error('Error formatting date:', error);
      return ''; // Return an empty string if an error occurs during formatting
    }
  }
  private formatTime(time: string): string {
    try {
      const formattedTime = this.datePipe.transform(new Date(`2000-01-01 ${time}`), 'hh:mm a');
      return formattedTime || ''; // Return an empty string if the format is invalid
    } catch (error) {
      console.error('Error formatting time:', error);
      return ''; // Return an empty string if an error occurs during formatting
    }
  }

  // ----------------------------------------------------------------
  // ngOnInit function
  ngOnInit() {
    // Fetch doctor names on component initialization
    this.fetchDoctorNames();
    this.fetchPatientAppointments();
  }

  // ----------------------------------------------------------------
  // onDoctorChange function
  onDoctorChange() {
    // Log the selected doctor's name to the console
    console.log('Selected Doctor:', this.selectedDoctor);

    // Store the selected doctor's name in the variable
    this.doctorName = this.selectedDoctor;

    // Fetch available slots for the selected doctor
    if (this.selectedDoctor) {
      this.fetchAvailableSlots(this.selectedDoctor);
    }
  }

  // ----------------------------------------------------------------
  // onEditDoctorChange function
  onEditDoctorChange() {
    // Log the selected doctor's name to the console
    console.log('Selected Edit Doctor:', this.selectedEditDoctor);

    // Fetch available slots for the selected doctor for editing
    if (this.selectedEditDoctor) {
      this.fetchAvailableSlots(this.selectedEditDoctor);
    }
  }

  // ----------------------------------------------------------------
  // fetch functions

  // fetchDoctorNames function
  fetchDoctorNames() {
    this.http.get<any[]>('http://127.0.0.1:5000/clinic/view/doctorNames').subscribe(
      (response) => {
        this.doctorNames = response.map((doctor) => doctor.name);
        console.log('Doctor Names:', this.doctorNames);
      },
      (error) => {
        console.error('Error fetching doctor names:', error);
      }
    );
  }
  // ----------------------------------------------------------------
  // fetchPatientAppointments function
  fetchPatientAppointments() {
    // Make a GET request to fetch patient appointments
    this.http.get<any[]>('http://127.0.0.1:5000/clinic/view/patientAppointment').subscribe(
      (response) => {
        this.patientAppointments = response;
        console.log('Patient Appointments:', this.patientAppointments);
      },
      (error) => {
        console.error('Error fetching patient appointments:', error);
        // Handle errors as needed
      }
    );
  }
  // ----------------------------------------------------------------
  // fetchAvailableSlots function
  fetchAvailableSlots(doctorName: string) {
    // Log the constructed API URL to the console
    const apiUrl = `http://127.0.0.1:5000/clinic/view/AvailableSlots/${doctorName}`;
    console.log('Constructed API URL:', apiUrl);

    // Make a GET request to fetch available slots for the selected doctor
    this.http.get<any[]>(apiUrl).subscribe(
      (response) => {

        if (response.includes('No Available Slots to show')){
          console.log('No Available Slots to show');
          this.availableSlots = [];
          return;
        }
        // Map the response to keep date and hour separate
        this.availableSlots = response.map((slot) => {
          return {
            date: this.formatDate(slot.slotDate),
            hour: this.formatTime(slot.slotHour)
          };
        });

        console.log('Available Slots:', this.availableSlots);

        // If there are no available slots, set availableSlots to an empty array
        if (this.availableSlots.length === 0) {
          this.availableSlots = [];
        }
      },
      (error) => {
        console.error('Error fetching available slots:', error);
        // If there is an error, or no available slots, set availableSlots to an empty array
        this.availableSlots = [];
      }
    );
  }

  // ----------------------------------------------------------------
  // createAppointment function
  createAppointment() {
    // Implement logic to create a new appointment
    const apiUrl = 'http://127.0.0.1:5000/clinic/create/patientAppointment';

    // Check if selectedSlot is defined and has valid date and hour properties
    if (
      this.selectedSlot &&
      this.selectedSlot.date &&
      this.selectedSlot.hour
    ) {
      const formattedDate = this.formatDate(this.selectedSlot.date);
      const formattedTime = this.formatTime(this.selectedSlot.hour);

      // Check if formattedDate and formattedTime are not empty (invalid)
      if (formattedDate && formattedTime) {
        const requestData = {
          doctor: this.doctorName,
          slotDate: formattedDate,
          slotHour: formattedTime
        };

        this.http.post(apiUrl, requestData).subscribe(
          (response: any) => {
            console.log('Create Appointment Response:', response);
            console.log('Request Data:', requestData);

            // Update the patient appointments array to reflect the changes
            this.fetchPatientAppointments();
          },
          (error) => {
            console.error('Error creating appointment:', error);
          }
        );
      } else {
        console.error('Invalid date or time format');
      }
    } else {
      console.error('Invalid selectedSlot object or properties');
    }
  }

  // ----------------------------------------------------------------
  // openEditPopup function
  openEditPopup(appointment: any) {
    // Set the selected values for editing
    this.selectedEditDoctor = appointment.name;  // Change 'doctor' to 'name'
    this.selectedEditSlot = {
      date: this.formatDate(appointment.slotDate),
      hour: this.formatTime(appointment.slotHour)
    };

    this.doctor = this.selectedEditDoctor;
    this.slotDate = this.selectedEditSlot.date;
    this.slotHour = this.selectedEditSlot.hour;

    // log the original date and time and doctor name
    console.log('Original Doctor:', this.doctor);
    console.log('Original Date:', this.slotDate);
    console.log('Original Time:', this.slotHour);

    // log the selected values to the console
    console.log('Selected Edit Doctor:', this.selectedEditDoctor);
    console.log('Selected Edit Slot:', this.selectedEditSlot);

    // Show the edit pop-up and overlay
    this.isEditPopupVisible = true;
  }


  // ----------------------------------------------------------------
  // closePopup function
  closePopup() {
    // Clear selected values and hide the pop-up
    this.selectedEditDoctor = '';
    this.selectedEditSlot = '';
    this.isEditPopupVisible = false;
  }

  // ----------------------------------------------------------------
  // Save Changes for Edit Slot pop-up
  saveChanges() {
    // Check if the new values are selected
    if (!this.selectedEditDoctor || !this.selectedEditSlot) {
      console.error('New doctor or slot is not selected');
      // Handle the error or return from the function
      return;
    }

    // Format the original date and time
    const oldDoctor = this.doctor;
    const oldDate = this.slotDate;
    const oldTime = this.slotHour;

    // log the original date and time and doctor name
    console.log('Original Doctor:', oldDoctor);
    console.log('Original Date:', oldDate);
    console.log('Original Time:', oldTime);

    // Construct the request data to update only the date and time
    const requestData = {
      doctor: oldDoctor,
      slotDate: oldDate,
      slotHour: oldTime,
      newDoctor: this.selectedEditDoctor,
      newSlotDate: this.selectedEditSlot.date,
      newSlotHour: this.selectedEditSlot.hour
    };


    // log the request data
    console.log('Request Data:', requestData);

    // Make a PUT request to update the selected patient appointment
    const apiUrl = 'http://127.0.0.1:5000/clinic/update/patientAppointment';
    this.http.put(apiUrl, requestData).subscribe(
      (response: any) => {
        console.log('Update Appointment Response:', response);
        this.fetchPatientAppointments(); // Update the patient appointments array
      },
      (error) => {
        console.error('Error updating appointment:', error);
      });

    // Close the pop-up after saving changes
    this.closePopup();
  }

  // ----------------------------------------------------------------
  // cancelSlot function
  cancelSlot(slot: any) {
    // Check if slot has valid properties
    if (!slot || !slot.name || !slot.slotDate || !slot.slotHour) {
      console.error('Invalid slot object or properties:', slot);
      // Handle the error or return from the function
      return;
    }

    // Log the original values before formatting
    console.log('Original Date:', slot.slotDate);
    console.log('Original Time:', slot.slotHour);

    // Format the date and time
    const formattedDate = this.formatDate(slot.slotDate);
    const formattedTime = this.formatTime(slot.slotHour);

    // Check if formattedDate and formattedTime are not empty (invalid)
    if (formattedDate && formattedTime) {
      // Construct the request data
      const requestData = {
        doctor: slot.name,
        slotDate: formattedDate,
        slotHour: formattedTime
      };

      console.log('Date After format:', formattedDate);
      console.log('Time After format:', formattedTime);

      // Make a DELETE request to cancel the selected patient appointment
      const apiUrl = 'http://127.0.0.1:5000/clinic/cancel/patientAppointment';
      this.http.delete(apiUrl, { body: requestData }).subscribe(
        (response: any) => {
          console.log('Appointment Cancellation Response:', response);

          // Update the patient appointments array to reflect the changes
          this.fetchPatientAppointments();
        },
        (error) => {
          console.error('Error cancelling appointment:', error);
          // Handle errors as needed
        }
      );
    } else {
      console.error('Invalid date or time format');
      // Handle invalid date or time format as needed
    }
  }

}