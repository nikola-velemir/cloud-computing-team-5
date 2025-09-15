import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { AuthService } from '../../../infrastructure/auth/service/auth.service';
import { User } from '../../../infrastructure/auth/model/user.mode';
import { UserRole } from '../../../infrastructure/auth/model/user-role.model';
import {environment} from '../../../../environments/environement';
import {HttpClient} from '@angular/common/http';
import {LoginResponse} from '../model/login.response';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  private readonly apiUrl = `${environment.apiUrl}/auth/login`
  constructor(private authService: AuthService, private http: HttpClient) {}

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.apiUrl, { email, password }).pipe(
      tap((res) => {
        this.authService.setSession(res)
      })
    )
  }
}
