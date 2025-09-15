import { HttpClient, HttpParams } from '@angular/common/http';
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
    let params = new HttpParams().set('genreId', genreId);
    const url = `${environment.apiUrl}/discover-page/albums`;
    return this.http.get<AlbumsResponse>(url, { params });
  }

  getArtists(genreId: string): Observable<ArtistsResponse> {
    let params = new HttpParams().set('genreId', genreId);
    const url = `${environment.apiUrl}/discover-page/artists`;
    return this.http.get<ArtistsResponse>(url, { params });
  }

  getSongsByArtist(genreId: string, artistId: string) {
    let params = new HttpParams()
      .set('artistId', artistId)
      .set('genreId', genreId);
    const url = `${environment.apiUrl}/discover-page/songs`;
    return this.http.get<SongsResponse>(url, { params });
  }

  getSongsByAlbum(genreId: string, albumId: string) {
    let params = new HttpParams()
      .set('albumId', albumId)
      .set('genreId', genreId);
    const url = `${environment.apiUrl}/discover-page/songs`;
    return this.http.get<SongsResponse>(url, { params });
  }
}
