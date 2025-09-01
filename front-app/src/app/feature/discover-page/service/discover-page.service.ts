import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environement';
import { GenresResponse } from '../model/genres-response.model';

@Injectable({
  providedIn: 'root',
})
export class DiscoverPageService {
  private apiUrl = `${environment.apiUrl}/discover-page/genres`;
  constructor(private http: HttpClient) {}

  getGenres(): Observable<GenresResponse> {
    return this.http.get<GenresResponse>(this.apiUrl);
  }

  getAlbumsAndArtists(genreId: string) {
    const url = `${environment.apiUrl}/discover-page/artists-albums?genreId=${genreId}`;
    return this.http.get<GenresResponse>(this.apiUrl);
  }
}
