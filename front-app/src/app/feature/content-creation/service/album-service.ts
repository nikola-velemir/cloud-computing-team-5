import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Album } from '../model/album';
import { shareReplay } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AlbumService {
  private readonly URL =
    'https://085dccw3qd.execute-api.eu-north-1.amazonaws.com/dev/content/content-creation/albums';
  albums$: any;
  constructor(private http: HttpClient) {
    this.albums$ = this.getAlbums().pipe(shareReplay(1));
  }

  getAlbums() {
    return this.http.get<Album[]>(this.URL);
  }
}
