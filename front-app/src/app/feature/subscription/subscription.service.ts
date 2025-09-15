import { Injectable } from '@angular/core';
import { EntityType } from './model/EntityType.model';
import { Observable, of } from 'rxjs';
import { AuthService } from '../../infrastructure/auth/service/auth.service';
import { UserSubscribeRequest } from './model/UserSubscribe.request';
import { environment } from '../../../environments/environement';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class SubscriptionService {
  constructor(
    private authService: AuthService,
    private httpClient: HttpClient
  ) {}

  subscribe(entityType: EntityType, contentId: string): Observable<boolean> {
    const userId = this.authService.getUser()?.userId;
    if (userId) {
      const request: UserSubscribeRequest = {
        userId: userId,
        entityType: entityType,
        contentId: contentId,
      };
      const url = `${environment.apiUrl}/subscription/add`;
      return this.httpClient.post<boolean>(url, request);
    }
    return of(false);
  }

  unsubscribe(entityType: EntityType, contentId: string): Observable<boolean> {
    return of(false);
  }

  isSubscribed(entityType: EntityType, contentId: string): Observable<boolean> {
    const userId = this.authService.getUser()?.userId;
    if (userId) {
      const params = {
        userId: userId,
        entityType: entityType,
        contentId: contentId,
      };
      const url = `${environment.apiUrl}/subscription/`;
      return this.httpClient.get<boolean>(url, { params });
    }
    return of(false);
  }
}
