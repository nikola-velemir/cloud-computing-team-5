import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { AuthService } from '../../../infrastructure/auth/service/auth.service';
import { User } from '../../../infrastructure/auth/model/user.mode';
import { UserRole } from '../../../infrastructure/auth/model/user-role.model';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  constructor(private authService: AuthService) {}

  login(email: string, password: string) {
    console.log('Email: ' + email);
    console.log('Password: ' + password);
    if (email === 'admin@gmail.com') {
      const user: User = {
        userId: 1,
        email: email,
        firstName: 'admin',
        lastName: 'admin',
        role: UserRole.Admin,
      };
      this.authService.setUser(user);
    } else {
      const user: User = {
        userId: 2,
        email: email,
        firstName: 'Regular',
        lastName: 'Regular',
        role: UserRole.Regular,
      };
      this.authService.setUser(user);
    }
  }
}
