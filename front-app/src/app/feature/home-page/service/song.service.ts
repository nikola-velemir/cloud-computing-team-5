import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HomeSong } from '../model/home-song.mode';

@Injectable({
  providedIn: 'root',
})
export class SongService {
  constructor() {}

  getSongs(): Observable<HomeSong[]> {
    const mockSongs: HomeSong[] = [
      {
        id: '1',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Comfortably Numb',
      },
      {
        id: '2',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Bohemian Rhapsody',
      },
      {
        id: '3',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Stairway to Heaven',
      },
      {
        id: '4',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Hotel California',
      },
      {
        id: '5',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Smells Like Teen Spirit',
      },
      {
        id: '6',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Imagine',
      },
      {
        id: '7',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Hey Jude',
      },
      {
        id: '8',
        coverImage: 'https://via.placeholder.com/150',
        title: 'Wonderwall',
      },
    ];

    return of(mockSongs);
  }
}
