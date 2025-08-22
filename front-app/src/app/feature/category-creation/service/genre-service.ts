import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  constructor() {}

  createGenre(obj: any): Observable<any> {
    return of({});
  }
}
