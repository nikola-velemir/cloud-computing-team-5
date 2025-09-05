import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environement';
import { GenreCreationRequest } from '../model/GenreCreationRequest';
import { GenreIconUploadRequest } from '../model/GenreIconUploadRequest';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  private readonly URL = environment.apiUrl + '/genre-creation';
  constructor(private http: HttpClient) {}

  uploadGenreIcon(url: string, file: File) {
    const headers = new HttpHeaders({
      'Content-Type': file.type,
    });

    return this.http.put(url, file, { headers });
  }
  requestGenreIconUpload(request: GenreIconUploadRequest) {
    return this.http.put<{ uploadUrl: string }>(this.URL, request);
  }
  createGenre(request: GenreCreationRequest) {
    return this.http.post<{ genreId: string }>(this.URL, request);
  }
}
