import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environement';
import { ArtistViewResponse } from '../model/artist-view-response';

@Injectable({
  providedIn: 'root',
})
export class PerformerViewService {
  private readonly BASE_URL = environment.apiUrl + '/content-preview/artist';
  getPerformer(id: any) {
    return this.http.get<ArtistViewResponse>(`${this.BASE_URL}/${id}`);
  }
  constructor(private http: HttpClient) {}
}
