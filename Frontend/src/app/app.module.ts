import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ListUsersComponent } from './users/list-users/list-users.component';
import { GetAllPatientsComponent } from './patients/get-all-patients/get-all-patients.component';
import { GetAllMedicalStaffComponent } from './medical-staff/get-all-medical-staff/get-all-medical-staff.component';


@NgModule({
  declarations: [
    AppComponent,
    ListUsersComponent,

    GetAllPatientsComponent,
      GetAllMedicalStaffComponent

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
