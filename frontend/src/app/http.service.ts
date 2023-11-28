import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  header = { Authorization: `Bearer ${localStorage.getItem('token')}`}

  constructor(private http: HttpClient) { }

  get<T>(url: string) {
    return this.http.get<T>(url, { headers: this.header, observe: 'response' }).pipe(map((response:  any) => {
      return response.body;
    }));
  }

  post<T>(url: string, payload: any) {
    return this.http.post<T>(url, payload, { headers: this.header });
  }

  delete<T>(url: string) {
    return this.http.delete<T>(url, { headers: this.header });
  }
}
