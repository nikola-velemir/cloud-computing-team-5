import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AlbumsResponse } from '../model/albums.response';
import { environment } from '../../../../environments/environement';
import { GenresResponse } from '../model/genres.response';
import { SongsResponse } from '../model/song.response';

@Injectable({
  providedIn: 'root',
})
export class ContentManagementService {
  constructor(private httpClient: HttpClient) {}

  loadAlbums(
    limit: number = 10,
    nextToken?: string
  ): Observable<AlbumsResponse> {
    const url = `${environment.apiUrl}/home-page/albums`;
    let params = new HttpParams().set('limit', limit.toString());
    if (nextToken) {
      params = params.set('lastKey', nextToken);
    }
    return this.httpClient.get<AlbumsResponse>(url, { params });
  }

  loadGenres(
    limit: number = 10,
    nextToken?: string
  ): Observable<GenresResponse> {
    const url = `${environment.apiUrl}/home-page/genres`;
    let params = new HttpParams().set('limit', limit.toString());
    if (nextToken) {
      params = params.set('lastKey', nextToken);
    }
    return this.httpClient.get<GenresResponse>(url, { params });
  }

  loadSongs(limit: number = 10, nextToken?: string): Observable<SongsResponse> {
    const url = `${environment.apiUrl}/home-page/songs`;
    let params = new HttpParams().set('limit', limit.toString());
    if (nextToken) {
      params = params.set('lastKey', nextToken);
    }
    return this.httpClient.get<SongsResponse>(url, { params });
  }

  deleteAlbum(id: string): Observable<boolean> {
    const url = `${environment.apiUrl}/content-delete/album/${id}`;
    return this.httpClient.delete<boolean>(url);
  }
}
