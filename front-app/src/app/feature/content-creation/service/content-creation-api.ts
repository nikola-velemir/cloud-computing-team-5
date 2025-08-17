import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {of} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ContentCreationApi {

  constructor(private http: HttpClient) {
  }

  createAsSingles() {
    return of(0);
  }

  createOnNewAlbum() {
    return of(1);
  }

  createWithAlbum() {
    return of(2);
  }
}
