import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HomeArtist } from '../model/home-artist.model';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  constructor() {}

  getArtists(): Observable<HomeArtist[]> {
    const mockArtists: HomeArtist[] = [
      {
        id: '1',
        firstName: 'David',
        lastName: 'Gilmour',
        image: 'https://via.placeholder.com/150',
      },
      {
        id: '2',
        firstName: 'Roger',
        lastName: 'Waters',
        image: 'https://via.placeholder.com/150',
      },
      {
        id: '3',
        firstName: 'Richard',
        lastName: 'Wright',
        image: 'https://via.placeholder.com/150',
      },
      {
        id: '4',
        firstName: 'David',
        lastName: 'Wright',
        image: 'https://via.placeholder.com/150',
      },
    ];

    return of(mockArtists);
  }
}
