import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HomeAlbum } from '../model/home-album.model';

@Injectable({
  providedIn: 'root',
})
export class AlbumService {
  constructor() {}
  getAlbums(): Observable<HomeAlbum[]> {
    const albums: HomeAlbum[] = [
      {
        id: '1',
        title: 'Dark Side of the Moon',
        coverImage: 'https://via.placeholder.com/300',
      },
      {
        id: '2',
        title: 'Abbey Road',
        coverImage: 'https://via.placeholder.com/300',
      },
      {
        id: '3',
        title: 'Thriller',
        coverImage: 'https://via.placeholder.com/300',
      },
      {
        id: '4',
        title: 'Back in Black',
        coverImage: 'https://via.placeholder.com/300',
      },
    ];

    return of(albums);
  }
}
