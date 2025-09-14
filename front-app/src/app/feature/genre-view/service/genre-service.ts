import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environement';
import { GenrePreviewResponse } from '../model/model';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  private readonly BASE_URL = environment.apiUrl + '/content-preview/genre';
  constructor(private http: HttpClient) {}

  getGenre(id: string) {
    return this.http.get<GenrePreviewResponse>(`${this.BASE_URL}/${id}`);
  }
}
