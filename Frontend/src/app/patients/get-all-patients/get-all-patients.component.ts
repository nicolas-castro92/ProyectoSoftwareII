import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-get-all-patients',
  templateUrl: './get-all-patients.component.html',
  styleUrls: ['./get-all-patients.component.css']
})
export class GetAllPatientsComponent {
  dataList: any[] = [];

  constructor(private http: HttpClient) {
    this.getPatientsFromBackend();
  }

  getPatientsFromBackend() {
    this.http.get<any[]>('http://localhost:8000/patients/all_user_patient_familiar').subscribe(data => {
      this.dataList = data;
    });
  }

  eliminarPaciente(id: number) {
    this.http.delete<any[]>(`http://localhost:8000/patients/delete_patient/${id}`).subscribe(() => {
      this.dataList = this.dataList.filter((u) => u.id !== id);
    })
  }
}
