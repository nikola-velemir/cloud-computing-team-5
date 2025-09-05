import { Injectable } from '@angular/core';
import { RegisterRequest } from '../model/register.request';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {
  constructor() {}

  register(data: RegisterRequest): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }
}
