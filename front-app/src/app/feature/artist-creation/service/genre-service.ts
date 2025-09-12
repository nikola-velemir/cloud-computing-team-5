import { Injectable } from '@angular/core';
import {environment} from '../../../../environments/environement';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ListGenres} from '../model/list-genres';

@Injectable({
  providedIn: 'root'
})
export class GenreService {
  private apiUrl = `${environment.apiUrl}/discover-page/genres`;
  constructor(private http:HttpClient) { }

  getAllGenres():Observable<ListGenres>{
      return this.http.get<ListGenres>(this.apiUrl);
  }
}
