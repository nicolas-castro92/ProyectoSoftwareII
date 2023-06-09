import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-get-all-medical-staff',
  templateUrl: './get-all-medical-staff.component.html',
  styles: [
  ]
})
export class GetAllMedicalStaffComponent {
  dataList: any[] = [];

  constructor(private http: HttpClient) {
    this.getPatientsFromBackend();
  }

  getPatientsFromBackend() {
    this.http.get<any[]>('http://localhost:8000/medical_staff/get_all_medical_staff').subscribe(data => {
      this.dataList = data;
    });
  }

}
