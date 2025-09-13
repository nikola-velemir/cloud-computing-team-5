// auth.interceptor.fn.ts
import { inject } from '@angular/core';
import {
  HttpRequest,
  HttpHandlerFn,
  HttpEvent,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthService } from '../auth/service/auth.service';
import { Router } from '@angular/router';

export function AuthInterceptor(
  req: HttpRequest<any>,
  next: HttpHandlerFn
): Observable<HttpEvent<any>> {
  const authService = inject(AuthService);
  const router = inject(Router);

  console.log('Interceptor called for URL:', req.url);

  const token = authService.getToken();

  let authReq = req;
  if (req.url.includes('s3.amazonaws.com')) {
    console.log('AA');
    return next(req); // skip Authorization
  }
  if (token) {
    authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    });
    console.log(
      'Interceptor added token:',
      authReq.headers.get('Authorization')
    );
  }

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        authService.logOut();
        router.navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
}
