import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, shareReplay } from 'rxjs';
import { Genre } from '../model/genre';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  genres$;
  private readonly URL =
    'https://085dccw3qd.execute-api.eu-north-1.amazonaws.com/dev/content/content-creation/genres';
  constructor(private http: HttpClient) {
    this.genres$ = this.getGenres().pipe(shareReplay(1));
  }

  getGenres(): Observable<Genre[]> {
    return this.http.get<Genre[]>(`${this.URL}`);
  }
}
