// doctor-page.component.ts

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-doctor-page',
  templateUrl: './doctor-page.component.html',
  styleUrls: ['./doctor-page.component.css']
})
export class DoctorPageComponent implements OnInit {
  welcomeMessage = 'Welcome, Doctor';
  slots: any[] = [];
  newSlotDate: string = '';
  newSlotHour: string = '';

  isEditPopupVisible: boolean = false;
  selectedEditSlot: any = '';

  doctorNotifications: any[] = [];

  constructor(private http: HttpClient, private datePipe: DatePipe) { }

  // ----------------------------------------------------------------
  // ngOnInit function
  ngOnInit() {
    this.viewDoctorSlots();
  }

  // ----------------------------------------------------------------
  // Functions
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

  // ----------------------------------------------------------------
  fetchingNotifications: boolean = false;

  // Method to fetch doctor notifications
  fetchDoctorNotifications() {
    this.fetchingNotifications = true;

    // Make a GET request to fetch doctor notifications
    const apiUrl = 'http://127.0.0.1:5000/clinic/notify/doctor';

    this.http.get<any>(apiUrl).subscribe(
      (notification) => {
        // Check if the new notification is the same as the last one
        if (!this.isDuplicateNotification(notification)) {
          // Add the new notification to the array
          this.doctorNotifications.push(notification);
        } else {
          console.log('No new notifications.');
        }
      },
      (error) => {
        console.error('Error fetching doctor notifications:', error);
        this.doctorNotifications.push("No new notifications");
      },
      () => {
        // This block will be executed when the observable completes (whether it's an error or not)
        this.fetchingNotifications = false;
      }
    );
  }

  // Method to check if a notification is a duplicate
  isDuplicateNotification(newNotification: any): boolean {
    // Check if the new notification is the same as any notification in the array
    for (const notification of this.doctorNotifications) {
      if (JSON.stringify(notification) === JSON.stringify(newNotification)) {
        return true; // If a match is found, return true
      }
    }
    return false; // If no match is found, return false
  }


  // ----------------------------------------------------------------
  // Add a new slot
  addNewSlot() {
    // Check if newSlotDate and newSlotHour are not empty
    if (this.newSlotDate && this.newSlotHour) {
      // Format the new slot hour using the DatePipe
      const formattedHour = this.datePipe.transform(new Date(`2000-01-01 ${this.newSlotHour}`), 'hh:mm a');

      // Check if formattedHour is not empty (invalid)
      if (formattedHour) {
        // Construct the new slot object
        const newSlot = {
          slotDate: this.newSlotDate,
          slotHour: formattedHour
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
        console.error('Invalid time format');
        // Handle invalid time format as needed
      }
    } else {
      // Handle case where date or hour is empty
      console.error('Date and Hour are required');
      // You can show a message to the user or perform other actions
    }
  }

  // ----------------------------------------------------------------
  // Open the Edit Slot pop-up
  openEditPopup(slot: any) {
    // Set the selected slot for editing
    this.selectedEditSlot = {
      slotDate: slot.slotDate,
      slotHour: slot.slotHour
    };

    // Show the edit pop-up and overlay
    this.isEditPopupVisible = true;
  }

  // Save Changes for Edit Slot pop-up
  saveChanges() {
    // Check if the new values are selected
    if (!this.selectedEditSlot) {
      console.error('Slot is not selected for editing');
      // Handle the error or return from the function
      return;
    }

    // Format the original date
    const formattedOriginalDate = new Date(this.selectedEditSlot.slotDate).toISOString().split('T')[0];
    console.log('Formatted Original Date:', formattedOriginalDate);

    // Check if newSlotDate and newSlotHour are not empty
    if (this.newSlotDate && this.newSlotHour) {
      // Format the new date and time
      const formattedNewDate = new Date(this.newSlotDate).toISOString().split('T')[0];
      const formattedNewTime = this.datePipe.transform(new Date(`2000-01-01 ${this.newSlotHour}`), 'hh:mm a');

      // Construct the request data
      const requestData = {
        slotDate: formattedOriginalDate,
        slotHour: this.selectedEditSlot.slotHour,
        newSlotDate: formattedNewDate,
        newSlotHour: formattedNewTime
      };

      // Make a PUT request to update the selected slot
      const apiUrl = 'http://127.0.0.1:5000/clinic/update/doctorSlot';
      this.http.put(apiUrl, requestData).subscribe(
        (response: any) => {
          console.log('Update Slot Response:', response);

          // Update the slots array to reflect the changes
          this.viewDoctorSlots();
        },
        (error) => {
          console.error('Error updating slot:', error);
          // Handle errors as needed
        });

      // Close the pop-up after saving changes
      this.closePopup();
    } else {
      // Handle case where date or hour is empty
      console.error('New Date and New Hour are required');
      // You can show a message to the user or perform other actions
    }
  }

  // ----------------------------------------------------------------
  // Close the Edit Slot pop-up
  closePopup() {
    // Clear selected values and hide the pop-up
    this.selectedEditSlot = '';
    this.isEditPopupVisible = false;
  }

  // ----------------------------------------------------------------
  // Delete Slot
  cancelSlot(slot: any) {
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
        this.viewDoctorSlots();
      },
      (error) => {
        console.error('Error cancelling slot:', error);
      }
    );
  }
}
