import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-create-medical-staff',
  templateUrl: './create-medical-staff.component.html',
  styles: [
  ]
})
export class CreateMedicalStaffComponent {
  constructor(private http: HttpClient) { }

  crearFamiliar(event: Event) {

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
    const especialidad = form['specialty'].value;
    const tipo_personal = form['personal_type'].value;


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

    this.http.post('http://localhost:8000/medical_staff/create_user_with_medical_staff_medical_staff_create_user_with_medical_staff_post', body)
      .subscribe(
        (response) => {
          console.log('Usuario y familiar creados correctamente', response);
          form.reset();
        },
        (error) => {
          console.error('Error al crear el usuario y familiar', error);
        }
      );
  }

}
