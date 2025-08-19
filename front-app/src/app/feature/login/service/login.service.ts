import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  constructor() {}

  login(email: string, password: string) {
    console.log('Email: ' + email);
    console.log('Password: ' + password);
  }
}
