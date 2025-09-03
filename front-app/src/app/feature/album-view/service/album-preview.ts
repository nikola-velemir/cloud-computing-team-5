import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environement';
import { AlbumViewResponse } from '../model/album-view-response';

@Injectable({
  providedIn: 'root',
})
export class AlbumPreviewService {
  private readonly BASE_URL = environment.apiUrl + '/content-preview/album';
  constructor(private http: HttpClient) {}

  getAlbumForView(albumId: string) {
    return this.http.get<AlbumViewResponse>(`${this.BASE_URL}/${albumId}`);
  }
}
