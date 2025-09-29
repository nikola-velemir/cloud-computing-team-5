import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Artist } from '../model/artist.mode';
import { environment } from '../../../../environments/environement';
import { catchError, Observable, of, throwError } from 'rxjs';
import { UpdateArtistRequest } from '../model/update-artist.request';

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

  updateArtist(artist: UpdateArtistRequest): Observable<any> {
    console.log(artist);
    return this.httpClient
      .post(`${environment.apiUrl}/content-update/artist`, artist)
      .pipe(
        catchError((err) => {
          console.log(err);
          const customError = {
            error: err.error,
          };
          console.log(customError);
          return throwError(customError);
        })
      );
  }
}
