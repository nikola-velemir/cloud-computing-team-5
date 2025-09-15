import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Track } from '../model/track';
import { AlbumMetadata } from '../model/album';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environement';

@Injectable({
  providedIn: 'root',
})
export class AudioApi {
  private readonly BASE_URL = environment.apiUrl;
  constructor(private http: HttpClient) {}

  getTrack(trackId: string): Observable<Track> {
    return this.http.get<Track>(
      `${this.BASE_URL}/content-player/get-track/${trackId}`
    );
  }

  getAlbum(albumId: string): Observable<AlbumMetadata> {
    return this.http.get<AlbumMetadata>(
      `${this.BASE_URL}/content-player/get-album/${albumId}`
    );
  }
}
