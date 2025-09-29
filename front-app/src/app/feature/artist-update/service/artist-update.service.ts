import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Artist } from '../model/artist.mode';
import { environment } from '../../../../environments/environement';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ArtistUpdateService {
  constructor(private httpClient: HttpClient) {}

  getGenres() {}

  getArtist(artistId: string): Observable<Artist> {
    return this.httpClient.get<Artist>(
      `${environment.apiUrl}/content-preview/artist/${artistId}`
    );
  }

  updateArtist(artist: Artist) {}
}
