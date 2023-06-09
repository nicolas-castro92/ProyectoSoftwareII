import { Component } from '@angular/core';
import { ListUsersComponent } from './users/list-users/list-users.component';
import { CreatePatientComponent } from './patients/create-patient/create-patient.component';
import { CreateFamiliarComponent } from './familiars/create-familiar/create-familiar.component';
import { GetAllPatientsComponent} from './patients/get-all-patients/get-all-patients.component';
import { CreateMedicalStaffComponent } from './medical-staff/create-medical-staff/create-medical-staff.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  componenteSeleccionado: any;

  listarUsuarios() {
    this.componenteSeleccionado = ListUsersComponent;
  }

  registrarFamiliar(){
    this.componenteSeleccionado = CreateFamiliarComponent;
  }

  registrarPaciente(){
    this.componenteSeleccionado = CreatePatientComponent;
  }

  listarPacientes(){
    this.componenteSeleccionado = GetAllPatientsComponent;
  }


  registrarPersonalMedico(){
    this.componenteSeleccionado = CreateMedicalStaffComponent;
  }

}
