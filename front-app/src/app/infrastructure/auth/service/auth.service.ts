import { Injectable } from '@angular/core';
import { BehaviorSubject, map, Observable } from 'rxjs';
import { User } from '../model/user.mode';
import { UserRole } from '../model/user-role.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUser = new BehaviorSubject<User | null>(this.getStoredUser());
  private token = new BehaviorSubject<string | null>(this.getStoredToken());

  currentUser$: Observable<User | null> = this.currentUser.asObservable();

  loggedIn$: Observable<boolean> = this.currentUser$.pipe(
    map((user) => user !== null)
  );

  userRole$: Observable<UserRole> = this.currentUser$.pipe(
    map((user) => user?.role ?? UserRole.Unauthenticated)
  );

  getUser(): User | null {
    return this.currentUser.getValue();
  }

  setUser(user: User | null) {
    if (typeof window !== 'undefined') {
      if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
      } else {
        localStorage.removeItem('currentUser');
      }
    }
    this.currentUser.next(user);
  }

  private getStoredUser(): User | null {
    if (typeof window === 'undefined') return null;
    const storedUser = localStorage.getItem('currentUser');
    return storedUser ? JSON.parse(storedUser) : null;
  }

  getToken(): string | null {
    return this.token.getValue();
  }

  setToken(token: string | null) {
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('jwt', token);
      } else {
        localStorage.removeItem('jwt');
      }
    }
    this.token.next(token);
  }

  private getStoredToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('jwt');
  }

  logOut() {
    this.setUser(null);
    this.setToken(null);
  }
}
