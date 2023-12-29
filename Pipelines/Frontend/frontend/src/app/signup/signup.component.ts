// signup.component.ts

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

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
      apiUrl = '127.0.0.1:5000/clinic/signup/doctor';
    } else if (this.userType === 'patient') {
      // Add conditions for other user types if needed
      apiUrl = '127.0.0.1:5000/clinic/signup/patient';
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
        console.log('Sign Up Response:', JSON.stringify(response));

        // Navigate to the login page
        if (JSON.stringify(response).includes('You already registered, Please log in')){
          window.alert('You already registered, Please log in');
          this.router.navigate(['/signin']);
        }
        else{
          if(this.userType === 'doctor'){
            window.alert('You have successfully registered, Welcome to the clinic Doctor');
            this.router.navigate(['/doctor']);
          }
          else if(this.userType === 'patient'){
            window.alert('You have successfully registered, Welcome to the clinic Patient');
            this.router.navigate(['/patient']);
          }
        }

        // You can also use the below condition to redirect based on userType
      },
      (error) => {
        console.error('Sign Up failed:', error);
        // You can handle errors here
        if (error === 'You already registered, Please log in'){
          window.alert('You already registered, Please log in');

        }
      }
    );
  }
}
