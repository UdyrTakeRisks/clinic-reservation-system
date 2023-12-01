import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';


import { HttpClientModule } from '@angular/common/http'; // Import the UserService

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SigninComponent } from './signin/signin.component';
import { SignupComponent } from './signup/signup.component';
import { DoctorPageComponent } from './doctor-page/doctor-page.component';
import { PatientPageComponent } from './patient-page/patient-page.component';


@NgModule({
  declarations: [
    AppComponent,
    SigninComponent,
    SignupComponent,
    DoctorPageComponent,
    PatientPageComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [
    DatePipe,
  ], // Add the UserService to providers
  bootstrap: [AppComponent]
})
export class AppModule { }
