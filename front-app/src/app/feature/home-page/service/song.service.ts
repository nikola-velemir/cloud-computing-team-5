import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { SongsResponse } from '../model/songs-response.model';
import { environment } from '../../../../environments/environement';

@Injectable({
  providedIn: 'root',
})
export class SongService {
  private apiUrl = `${environment.apiUrl}/home-page/songs`;

  constructor(private httpClient: HttpClient) {}

  getSongs(limit: number = 10, nextToken?: string): Observable<SongsResponse> {
    let params = new HttpParams().set('limit', limit.toString());
    if (nextToken) {
      params = params.set('lastKey', nextToken);
    }
    return this.httpClient.get<SongsResponse>(this.apiUrl, { params });
  }
}
