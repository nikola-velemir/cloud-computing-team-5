import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, shareReplay } from 'rxjs';
import { Genre } from '../model/genre';
import { environment } from '../../../../environments/environement';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  genres$;
  private readonly URL = environment.apiUrl + '/content-creation/genres';
  constructor(private http: HttpClient) {
    this.genres$ = this.getGenres().pipe(shareReplay(1));
  }

  getGenres(): Observable<Genre[]> {
    return this.http.get<Genre[]>(`${this.URL}`);
  }
}
