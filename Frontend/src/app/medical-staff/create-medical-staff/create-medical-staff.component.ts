import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-create-medical-staff',
  templateUrl: './create-medical-staff.component.html',
  styleUrls: ['./create-medical-staff.component.css']
})
export class CreateMedicalStaffComponent {
  constructor(private http: HttpClient) { }
   
  crearPersonalMedico(event: Event) {

    console.log('Tipo de evento:', event.type);
    console.log('Objeto del evento:', event);
    event.preventDefault();

    const form = event.target as HTMLFormElement;
  
    const nombre = form['nombre'].value;
    const apellido = form['apellido'].value;
    const cedula = form['cedula'].value;
    const edad = form['edad'].value;
    const telefono = form['telefono'].value;
    const correo = form['correo'].value;
    const direccion = form['direccion'].value;
    const tarjeta_profesional = form['tarjeta_profesional'].value;
    const especialidad = form['especialidad'].value;
    const tipo_personal = form['tipo_personal'].value;


    const body = {
      name: nombre,
      last_name: apellido,
      identification_card: cedula,
      age: edad,
      phone: telefono,
      email: correo,
      address: direccion,
      professional_card: tarjeta_profesional,
      specialty: especialidad,
      personal_type:tipo_personal
    };

    this.http.post('http://localhost:8000/medical_staff/create_user_with_medical_staff', body)
      .subscribe(
        (response) => {
          console.log('Usuario y Personal Medico  creados correctamente', response);
          form.reset();
        },
        (error) => {
          console.error('Error al crear el usuario y Personal Medico', error);
        }
      );
      
  }
}
