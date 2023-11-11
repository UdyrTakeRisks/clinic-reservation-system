// patient-page.component.ts

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-patient-page',
  templateUrl: './patient-page.component.html',
  styleUrls: ['./patient-page.component.css']
})
export class PatientPageComponent implements OnInit {
  welcomeMessage = 'Welcome, Patient'; // Replace with actual patient name
  availableSlots: any[] = [];
  doctorNames: string[] = [];
  selectedDoctor: string = '';
  selectedSlot: any = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Fetch doctor names on component initialization
    this.fetchDoctorNames();
  }

  fetchDoctorNames() {
    // Make a GET request to fetch doctor names
    this.http.get<string[]>('http://127.0.0.1:5000/clinic/view/doctorNames').subscribe(
      (response) => {
        this.doctorNames = response;
        console.log('Doctor Names:', this.doctorNames);
      },
      (error) => {
        console.error('Error fetching doctor names:', error);
        // Handle errors as needed
      }
    );
  }

  onDoctorChange() {
    // Fetch available slots for the selected doctor
    if (this.selectedDoctor) {
      this.fetchAvailableSlots(this.selectedDoctor);
    }
  }

  fetchAvailableSlots(doctorName: string) {
    // Make a GET request to fetch available slots for the selected doctor
    const apiUrl = `http://127.0.0.1:5000/clinic/view/AvailableSlots/${doctorName}`;
    this.http.get<any[]>(apiUrl).subscribe(
      (response) => {
        this.availableSlots = response;
        console.log('Available Slots:', this.availableSlots);
      },
      (error) => {
        console.error('Error fetching available slots:', error);
        // Handle errors as needed
      }
    );
  }

  createAppointment() {
    // Implement logic to create a new appointment
    const apiUrl = 'http://127.0.0.1:5000/clinic/create/patientAppointment';

    const requestData = {
      doctor: this.selectedDoctor,
      slotDate: this.selectedSlot.date,
      slotHour: this.selectedSlot.hour
    };

    this.http.post(apiUrl, requestData).subscribe(
      (response: any) => {
        console.log('Create Appointment Response:', response);

        // Optionally, you can update the available slots array to reflect the changes
        // this.fetchAvailableSlots(this.selectedDoctor);
      },
      (error) => {
        console.error('Error creating appointment:', error);
        // Handle errors as needed
      }
    );
  }

  editSlot(slot: any) {
    // Implement logic to edit the selected slot
  }

  cancelSlot(slot: any) {
    // Implement logic to cancel the selected slot
    const apiUrl = 'http://127.0.0.1:5000/clinic/cancel/patientAppointment';

    const requestData = {
      doctor: slot.doctorName,
      slotDate: slot.date,
      slotHour: slot.hour
    };

    this.http.post(apiUrl, requestData).subscribe(
      (response: any) => {
        console.log('Cancel Slot Response:', response);

        // Update the available slots array to reflect the changes
        this.fetchAvailableSlots(this.selectedDoctor);
      },
      (error) => {
        console.error('Error canceling slot:', error);
        // Handle errors as needed
      }
    );
  }
}
