import { Injectable } from '@angular/core';
import { RegisterRequest } from '../model/register.request';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {
  constructor() {}

  register(registerRequest: RegisterRequest) {
    const formData = new FormData();
    formData.append('firstName', registerRequest.firstName);
    formData.append('lastName', registerRequest.lastName);
    formData.append('dateOfBirth', registerRequest.dateOfBirth);
    formData.append('username', registerRequest.username);
    formData.append('email', registerRequest.email);
    formData.append('password', registerRequest.password);

    for (const [key, value] of formData.entries()) {
      console.log(key, value);
    }
  }
}
