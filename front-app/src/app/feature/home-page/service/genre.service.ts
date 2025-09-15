import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environement';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GenresResponse } from '../model/genre-response.model';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  private apiUrl = `${environment.apiUrl}/home-page/genres`;

  constructor(private httpClient: HttpClient) {}

  getGenres(
    limit: number = 10,
    nextToken?: string
  ): Observable<GenresResponse> {
    let params = new HttpParams().set('limit', limit.toString());
    if (nextToken) {
      params = params.set('lastKey', nextToken);
    }
    return this.httpClient.get<GenresResponse>(this.apiUrl, { params });
  }
}
