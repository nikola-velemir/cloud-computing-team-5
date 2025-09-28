import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { FeedCardData } from '../model/feed-card.model';
import { FeedType } from '../model/feed-type.mode';
import {HttpClient} from '@angular/common/http';
import {AuthService} from '../../../infrastructure/auth/service/auth.service';
import {environment} from '../../../../environments/environement';

@Injectable({
  providedIn: 'root',
})
export class FeedService {
  constructor(private httpClient: HttpClient, private authService:AuthService) {}

  getFeed(): Observable<FeedCardData[]> {
    const userId = this.authService.getUser()?.userId;
    if (userId) {
      const params = {
        userId: userId,
      };
      const url = `${environment.apiUrl}/feed`;
      return this.httpClient.get<FeedCardData[]>(url, {params});
    }
    return of([]);
    }
}
