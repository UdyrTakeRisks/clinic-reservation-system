// signin.component.ts

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  fullName: string = '';
  password: string = '';
  userType: string = '';
  errorMessage: string = ''; // New variable to store error messages

  constructor(private router: Router, private http: HttpClient) { }

  signIn() {
    // Conditionally construct the API URL based on userType
    let apiUrl = '';
    if (this.userType === 'doctor') {
      apiUrl = environment.environmenturl + '/clinic/signin/doctor';
    } else if (this.userType === 'patient') {
      // Add conditions for other user types if needed
      apiUrl = environment.environmenturl + '/clinic/signin/patient';
    }

    console.log('API URL:', apiUrl);

    // Create the request body
    const body = {
      name: this.fullName,
      password: this.password
    };



    // Send a POST request to the backend API
    this.http.post(apiUrl, body).subscribe(
      (response: any) => {
        console.log('Sign In Response:', response);
        if (response === 'Please Doctor Register First') {
          this.router.navigate(['/signup']);
          window.alert('Please Doctor Register First');
        }
        else if (response === 'Please Patient Register First') {
          this.router.navigate(['/signup']);
          window.alert('Please Patient Register First');
        }
        else {
          if (this.userType === 'doctor') {
            this.router.navigate(['/doctor']);
          }
          else if (this.userType === 'patient') {
            this.router.navigate(['/patient']);
          }
        }
      },
      (error) => {
        console.error('Sign In failed:', error);
        this.errorMessage = 'Invalid credentials. Please try again.';
        window.alert(this.errorMessage);
      }
    );
  }
}
