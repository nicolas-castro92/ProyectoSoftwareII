import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateMedicalStaffComponent } from './create-medical-staff/create-medical-staff.component';
import { GetAllMedicalStaffComponent } from './get-all-medical-staff/get-all-medical-staff.component';



@NgModule({
  declarations: [
    CreateMedicalStaffComponent,
    GetAllMedicalStaffComponent
  ],
  imports: [
    CommonModule
  ]
})
export class MedicalStaffModule { }
