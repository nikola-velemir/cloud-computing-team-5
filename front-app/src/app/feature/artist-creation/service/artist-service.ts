import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../../environments/environement';
import { CreateArtistDTO } from '../model/create-artist-DTO';
import { catchError, Observable, throwError } from 'rxjs';
import { ArtistsResponse } from '../model/artists.response';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  private apiUrl = `${environment.apiUrl}/artist-creation/artists`;
  constructor(private http: HttpClient) {}

  createArtist(req: CreateArtistDTO): Observable<any> {
    console.log(req);
    return this.http.post(this.apiUrl, req).pipe(
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

  loadArtists(
    limit: number = 10,
    lastToken?: string
  ): Observable<ArtistsResponse> {
    const url = `${environment.apiUrl}/home-page/artists`;
    let params = new HttpParams().set('limit', limit.toString());
    if (lastToken) {
      params = params.set('lastToken', lastToken);
    }
    return this.http.get<ArtistsResponse>(url, { params });
  }

  deleteArtist(id: string): Observable<boolean> {
    const url = `${environment.apiUrl}/content-delete/artist/${id}`;
    return this.http.delete<boolean>(url);
  }
}
