import { HttpClient } from '@angular/common/http';
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

  uploadGenreIcon(url: string, file: File, contentType: string) {
    return this.http.put(url, file, {
      headers: {
        'Content-Type': contentType,
      },
      reportProgress: true,
    });
  }
  requestGenreIconUpload(request: GenreIconUploadRequest) {
    return this.http.post<{ uploadUrl: string; contentType: string }>(
      this.URL + '/request-url',
      request
    );
  }
  createGenre(request: GenreCreationRequest) {
    return this.http.post<{ genreId: string }>(this.URL, request);
  }
}
