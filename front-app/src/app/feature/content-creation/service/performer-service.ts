import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Artist } from '../model/artist';
import { Observable, shareReplay } from 'rxjs';
import { environment } from '../../../../environments/environement';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  private readonly URL = environment.apiUrl + '/content-creation/artists';
  performers$: Observable<Artist[]>;

  constructor(private http: HttpClient) {
    this.performers$ = this.getPerformers().pipe(shareReplay(1));
  }

  getPerformers() {
    return this.http.get<Artist[]>(this.URL);
  }
}
