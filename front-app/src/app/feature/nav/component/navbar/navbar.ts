import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../../infrastructure/auth/service/auth.service';
import { map, Observable } from 'rxjs';
import { UserRole } from '../../../../infrastructure/auth/model/user-role.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: false,
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss',
})
export class Navbar {
  constructor(private authService: AuthService, private router: Router) {}

  get loggedIn$(): Observable<boolean> {
    return this.authService.loggedIn$;
  }

  get isAdmin$(): Observable<boolean> {
    return this.authService.userRole$.pipe(
      map((role) => role === UserRole.Admin)
    );
  }

  public logOut() {
    this.authService.logOut();
    this.router.navigate(['/']).then(() => {
      window.location.reload();
    });
  }
}
