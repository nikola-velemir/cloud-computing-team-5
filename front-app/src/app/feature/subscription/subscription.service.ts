import { Injectable } from '@angular/core';
import { EntityType } from './model/EntityType.model';
import { AuthService } from '../../infrastructure/auth/service/auth.service';
import { UserSubscribeRequest } from './model/UserSubscribe.request';
import { environment } from '../../../environments/environement';
import { HttpClient } from '@angular/common/http';
import {SubscriptionResponse} from './model/SubscriptionResponse';
import {Observable, of} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SubscriptionService {
  constructor(
    private authService: AuthService,
    private httpClient: HttpClient
  ) {}

  subscribe(entityType: EntityType, contentId: string, name:string,coverPath:string): Observable<boolean> {
    const user = this.authService.getUser();
    if (user) {
      const request = {
        userId: user.userId,
        userEmail: user.email,
        entityType: entityType,
        contentId: contentId,
        name: name,
        coverPath: coverPath,
      };
      const url = `${environment.apiUrl}/subscription/subscribe`;
      return this.httpClient.post<boolean>(url, request);
    }
    return of(false);
  }

  unsubscribe(entityType: EntityType, contentId: string, coverPath:string): Observable<boolean> {
    const user = this.authService.getUser();
    if (user) {
      const request = {
        userId: user.userId,
        entityType: entityType,
        contentId: contentId,
        coverPath: coverPath,
      };
      console.log(request);
      const url = `${environment.apiUrl}/subscription/unsubscribe`;
      return this.httpClient.delete<boolean>(url, { body: request });

    }
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
      const url = `${environment.apiUrl}/subscription/is-subscribed`;
      return this.httpClient.get<boolean>(url, { params });
    }
    return of(false);
  }

  getSubscribesByUser():Observable<SubscriptionResponse[]>{
    const userId = this.authService.getUser()?.userId;
    if (userId) {
      const params = {
        userId: userId,
      };
      const url = `${environment.apiUrl}/subscription/subscribe`;
      const res =  this.httpClient.get<SubscriptionResponse[]>(url, { params });
      console.log(res);
      return res;
    }
    return of([]);
  }
}
