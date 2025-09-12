// auth.interceptor.ts
import { inject, Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpErrorResponse,
  HttpInterceptorFn,
} from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { AuthService } from '../auth/service/auth.service';
import { Router } from '@angular/router';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();
  const authReq = attachAuthToken(req, token);
  console.log('A');
  return next(authReq).pipe(
    catchError((err) => {
      if (err.status === 401) {
        authService.logOut();
        router.navigate(['/login']);
      }
      return throwError(() => err);
    })
  );
};

const attachAuthToken = (
  req: HttpRequest<any>,
  token?: string | null
): HttpRequest<any> => {
  if (!token) return req;

  return req.clone({
    setHeaders: { Authorization: `Bearer ${token}` },
  });
};
