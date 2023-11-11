// doctor-page.component.ts

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-doctor-page',
  templateUrl: './doctor-page.component.html',
  styleUrls: ['./doctor-page.component.css']
})
export class DoctorPageComponent implements OnInit {
  welcomeMessage = 'Welcome, Doctor'; // Replace with actual doctor name
  slots: any[] = [];
  newSlotDate: string = '';
  newSlotHour: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Fetch doctor slots on component initialization
    this.viewDoctorSlots();
  }

  viewDoctorSlots() {
    // Make a GET request to fetch doctor slots
    this.http.get<any[]>('http://127.0.0.1:5000/clinic/view/doctorSlot').subscribe(
      (response) => {
        this.slots = response;
        console.log('Doctor Slots:', this.slots);
      },
      (error) => {
        console.error('Error fetching doctor slots:', error);
        // Handle errors as needed
      }
    );
  }

  addNewSlot() {
    // Check if newSlotDate and newSlotHour are not empty
    if (this.newSlotDate && this.newSlotHour) {
      // Construct the new slot object
      const newSlot = {
        slotDate: this.newSlotDate,
        slotHour: this.newSlotHour
      };

      // Send a POST request to add the new slot
      this.http.post<any>('http://127.0.0.1:5000/clinic/create/doctorSlot', newSlot).subscribe(
        (response) => {
          console.log('New slot added:', response);

          // Refresh the slots by fetching them again
          this.viewDoctorSlots();

          // Reset the input fields
          this.newSlotDate = '';
          this.newSlotHour = '';
        },
        (error) => {
          console.error('Error adding new slot:', error);
          // Handle errors as needed
        }
      );
    } else {
      // Handle case where date or hour is empty
      console.error('Date and Hour are required');
      // You can show a message to the user or perform other actions
    }
  }

  editSlot(slot: any) {
    // Implement logic to edit the selected slot
  }

  cancelSlot(slot: any) {
    // Make a DELETE request to cancel the selected slot
    const apiUrl = 'http://127.0.0.1:5000/clinic/cancel/doctorSlot';

    // Manually format the date to '%Y-%m-%d' format
    const formattedDate = new Date(slot.slotDate).toISOString().split('T')[0];

    const requestData = {
      slotDate: formattedDate,
      slotHour: slot.slotHour
    };

    this.http.delete(apiUrl, { body: requestData }).subscribe(
      (response: any) => {
        console.log('Slot Cancellation Response:', response);

        // Update the slots array to reflect the changes
        this.viewDoctorSlots();
      },
      (error) => {
        console.error('Error cancelling slot:', error);
        // Handle errors as needed
      }
    );
  }
}
