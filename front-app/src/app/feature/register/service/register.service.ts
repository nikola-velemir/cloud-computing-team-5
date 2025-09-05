import { Injectable } from '@angular/core';
import { RegisterRequest } from '../model/register.request';
import {environment} from '../../../../environments/environement';
import {AuthService} from '../../../infrastructure/auth/service/auth.service';
import {HttpClient} from '@angular/common/http';
import {catchError, Observable, throwError} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {
  private readonly apiUrl = `${environment.apiUrl}/auth/register`
  constructor(private authService: AuthService, private http: HttpClient) {}

  register(data: RegisterRequest): Observable<any> {
    return this.http.post(this.apiUrl, data).pipe(
      catchError((err) => {
        const errorMessage = err?.error?.error || 'Unknown error';
        console.error('Registration error:', errorMessage);

        return throwError(() => new Error(errorMessage));
      })
    );
  }
}
