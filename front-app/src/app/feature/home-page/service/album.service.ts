import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../../environments/environement';
import { AlbumsResponse } from '../model/album-response.model';

@Injectable({
  providedIn: 'root',
})
export class AlbumService {
  private apiUrl = `${environment.apiUrl}/home-page/albums`;

  constructor(private http: HttpClient) {}

  getAlbums(
    limit: number = 10,
    nextToken?: string
  ): Observable<AlbumsResponse> {
    let params = new HttpParams().set('limit', limit.toString());
    if (nextToken) {
      params = params.set('lastKey', nextToken);
    }
    return this.http.get<AlbumsResponse>(this.apiUrl, { params });
  }
}
