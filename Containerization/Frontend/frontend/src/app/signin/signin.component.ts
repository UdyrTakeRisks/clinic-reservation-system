// signin.component.ts

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  fullName: string = '';
  password: string = '';
  userType: string = '';

  constructor(private router: Router, private http: HttpClient) {}

  signIn() {
    // Conditionally construct the API URL based on userType
    let apiUrl = '';
    if (this.userType === 'doctor') {
      apiUrl = 'http://127.0.0.1:5000/clinic/signin/doctor';
    } else if (this.userType === 'patient') {
      // Add conditions for other user types if needed
      apiUrl = 'http://127.0.0.1:5000/clinic/signin/patient';
    }

    // Create the request body
    const body = {
      name: this.fullName,
      password: this.password
    };

    

    // Send a POST request to the backend API
    this.http.post(apiUrl, body).subscribe(
      (response: any) => {
        console.log('Sign In Response:', response);
        if (this.userType === 'doctor') {
          this.router.navigate(['/doctor']);
        }
        else if (this.userType === 'patient') {
          this.router.navigate(['/patient']);
        }
      },
      (error) => {
        console.error('Sign In failed:', error);
        // You can handle errors here
      }
    );
  }
}
