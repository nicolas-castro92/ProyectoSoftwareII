import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreatePatientComponent } from './create-patient/create-patient.component';
import { GetAllPatientsComponent } from './get-all-patients/get-all-patients.component';



@NgModule({
  declarations: [
    CreatePatientComponent,
    GetAllPatientsComponent
  ],
  imports: [
    CommonModule
  ]
})
export class PatientsModule { }
