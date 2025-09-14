import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router} from '@angular/router';
import {AuthService} from '../auth/service/auth.service';
import {UserRole} from '../auth/model/user-role.model';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router, private authService: AuthService) {}
  canActivate(route: ActivatedRouteSnapshot): boolean {
    const user = this.authService.getUser();
    const token = this.authService.getToken();
    const allowedRoles = route.data['roles'] as UserRole[];

    if (user && token) {
      if (!allowedRoles || allowedRoles.length === 0) {
        return true;
      }

      if (allowedRoles.includes(user.role)) {
        return true;
      }
    }

    this.router.navigate(['/login']);
    return false;
  }
}
