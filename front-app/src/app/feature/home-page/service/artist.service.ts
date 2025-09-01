import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { ArtistsResponse } from '../model/artists-response.model';
import { environment } from '../../../../environments/environement';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  constructor(private httpClient: HttpClient) {}
  private apiUrl = `${environment.apiUrl}/home-page/artists`;

  getArtists(
    limit: number = 10,
    nextToken?: string
  ): Observable<ArtistsResponse> {
    let params = new HttpParams().set('limit', limit.toString());
    if (nextToken) {
      params = params.set('lastToken', nextToken);
    }
    return this.httpClient.get<ArtistsResponse>(this.apiUrl, { params });
  }
}
