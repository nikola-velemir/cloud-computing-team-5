import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environement';
import { SongViewResponse } from '../model/song-view-response';

@Injectable({
  providedIn: 'root',
})
export class SongPreviewService {
  private readonly BASE_URL = environment.apiUrl + '/content-preview/song';
  constructor(private http: HttpClient) {}

  getSongPreview(id: string) {
    return this.http.get<SongViewResponse>(`${this.BASE_URL}/${id}`);
  }
}
