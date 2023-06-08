import { Component } from '@angular/core';
import { HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-list-users',
  templateUrl: './list-users.component.html',
  styleUrls: ['./list-users.component.css']
})
export class ListUsersComponent {
  dataList: any[] = [];

  constructor(private http: HttpClient){
    this.getDataFromBackend();
  }

  getDataFromBackend(){
    this.http.get<any[]>('http://localhost:8000/users/users').subscribe(data => {
      this.dataList = data;
    });
  }

  eliminarUsuario(id:number){
    this.http.delete<any[]>(`http://localhost:8000/users/users/${id}`).subscribe(()=> {
      this.dataList = this.dataList.filter((u)=>u.id !== id);
    })
  }
}
