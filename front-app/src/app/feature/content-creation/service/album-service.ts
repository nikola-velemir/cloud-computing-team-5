import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Album } from '../model/album';
import { shareReplay } from 'rxjs';
import { environment } from '../../../../environments/environement';

@Injectable({
  providedIn: 'root',
})
export class AlbumService {
  private readonly URL = environment.apiUrl + '/content-creation/albums';

  constructor(private http: HttpClient) {}

  getAlbums(artistIds: string[]) {
    return this.http.post<Album[]>(`${this.URL}/get-all`, { artistIds });
  }
}
