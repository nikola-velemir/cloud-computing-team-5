import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environement';
import { GenresResponse } from '../model/genres-response.model';
import { AlbumsResponse } from '../model/albums-response.model';
import { ArtistsResponse } from '../model/artists-response';
import { SongsResponse } from '../model/songs-response.model';

@Injectable({
  providedIn: 'root',
})
export class DiscoverPageService {
  constructor(private http: HttpClient) {}

  getGenres(): Observable<GenresResponse> {
    const url = `${environment.apiUrl}/discover-page/genres`;
    return this.http.get<GenresResponse>(url);
  }

  getAlbums(genreId: string): Observable<AlbumsResponse> {
    const url = `${environment.apiUrl}/discover-page/albums?genreId=${genreId}`;
    console.log(genreId);
    console.log(url);
    return this.http.get<AlbumsResponse>(url);
  }

  getArtists(genreId: string): Observable<ArtistsResponse> {
    const url = `${environment.apiUrl}/discover-page/artists?genreId=${genreId}`;
    return this.http.get<ArtistsResponse>(url);
  }

  getSongsByArtist(genreId: string, artistId: string) {
    const url = `${environment.apiUrl}/discover-page/song?artistId=${artistId}&genreId=${genreId}`;
    return this.http.get<SongsResponse>(url);
  }

  getSongsByAlbum(genreId: string, albumId: string) {
    const url = `${environment.apiUrl}/discover-page/artists?albumId=${albumId}&genreId=${genreId}`;
    return this.http.get<SongsResponse>(url);
  }
}
