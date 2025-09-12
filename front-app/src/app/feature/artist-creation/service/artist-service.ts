import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../../../environments/environement';
import {CreateArtistDTO} from '../model/create-artist-DTO';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ArtistService {
  private apiUrl = `${environment.apiUrl}/artist-creation/artists`;
  constructor(private http:HttpClient) { }

  createArtist(req: CreateArtistDTO):Observable<any>{
    console.log(req);
    return this.http.post(this.apiUrl, req);
  }
}
