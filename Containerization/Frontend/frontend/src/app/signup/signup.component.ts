// signup.component.ts

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  fullName: string = '';
  email: string = '';
  username: string = '';
  password: string = '';
  userType: string = '';

  constructor(private router: Router, private http: HttpClient) {}

  signUp() {
    // Conditionally construct the API URL based on userType
    let apiUrl = '';
    if (this.userType === 'doctor') {
      apiUrl = 'http://127.0.0.1:5000/clinic/signup/doctor';
    } else if (this.userType === 'patient') {
      // Add conditions for other user types if needed
      apiUrl = 'http://127.0.0.1:5000/clinic/signup/patient';
    }

    // Create the request body
    const body = {
      name: this.fullName,
      email: this.email,
      password: this.password
    };

    // Send a POST request to the backend API
    this.http.post(apiUrl, body).subscribe(
      (response: any) => {
        console.log('Sign Up Response:', response);

        // You can add logic for successful sign-up, such as navigating to a 'dashboard' page
        if (this.userType === 'doctor') {
          this.router.navigate(['/doctor']);
        }
        else if (this.userType === 'patient') {
          this.router.navigate(['/patient']);
        }
      },
      (error) => {
        console.error('Sign Up failed:', error);
        // You can handle errors here
      }
    );
  }
}
