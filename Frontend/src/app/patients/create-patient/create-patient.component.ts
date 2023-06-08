import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-create-patient',
  templateUrl: './create-patient.component.html',
  styleUrls: ['./create-patient.component.css']
})



export class CreatePatientComponent {

  constructor(private http:HttpClient){}

  crearFamiliar(event: Event){

    event.preventDefault();
    
    const form = event.target as HTMLFormElement;

    const nombre = form['nombre'].value;
    const apellido = form['apellido'].value;
    const cedula = form['cedula'].value;
    const edad = form['edad'].value;
    const telefono = form['telefono'].value;
    const correo = form['correo'].value;
    const direccion = form['direccion'].value;
    const idFamiliar = form['familiarId'].value;

    const body = {
      name: nombre,
      last_name: apellido,
      identification_card: cedula,
      age: edad,
      phone: telefono,
      email: correo,
      address: direccion,
      familiar_id: idFamiliar
    };

    this.http.post('http://localhost:8000/patients/create_user_with_patient_familiar', body)
      .subscribe(
        (response) => {
          console.log('Usuario y paciente creados correctamente', response);
          form.reset();
        },
        (error) => {
          console.error('Error al crear el usuario y familiar', error);
        }
      );
  }
}
