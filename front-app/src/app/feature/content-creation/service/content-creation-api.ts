import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ContentCreationApi {
  private readonly URL =
    'https://085dccw3qd.execute-api.eu-north-1.amazonaws.com/dev/content/content-creation';
  constructor(private http: HttpClient) {}

  createAsSingles() {
    return of(0);
  }

  createOnNewAlbum() {
    return of(1);
  }
  createAlbum(formData: FormData) {
    return this.http.post<{ albumId: string }>(this.URL + '/albums', formData);
  }
  createWithAlbum(formData: FormData) {
    return this.http.post(this.URL + '/songs/with-album', formData);
  }
}
