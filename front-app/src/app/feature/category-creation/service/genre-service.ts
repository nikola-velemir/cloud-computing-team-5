import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  private readonly URL =
    'https://085dccw3qd.execute-api.eu-north-1.amazonaws.com/dev/content/genre-creation';
  constructor(private http: HttpClient) {}

  createGenre(formData: FormData): Observable<any> {
    return this.http.post(this.URL, formData);
  }
}
