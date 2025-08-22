import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Artist } from '../model/artist';
import { Observable, shareReplay } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class PerformerService {
  private readonly URL =
    'https://085dccw3qd.execute-api.eu-north-1.amazonaws.com/dev/content/content-creation/performers';
  performers$: Observable<Artist[]>;

  constructor(private http: HttpClient) {
    this.performers$ = this.getPerformers().pipe(shareReplay(1));
  }

  getPerformers() {
    return this.http.get<Artist[]>(this.URL);
  }
}
