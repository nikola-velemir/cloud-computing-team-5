import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { FeedCardData } from '../model/feed-card.model';
import { FeedType } from '../model/feed-type.mode';

@Injectable({
  providedIn: 'root',
})
export class FeedService {
  constructor() {}

  getFeed(): Observable<FeedCardData[]> {
    const mockFeed: FeedCardData[] = [
      {
        id: '1',
        name: 'Album 1',
        type: FeedType.Album,
        image: 'https://via.placeholder.com/300x200',
      },
      {
        id: '2',
        name: 'Song 1',
        type: FeedType.Song,
        image: 'https://via.placeholder.com/300x200',
      },
      {
        id: '3',
        name: 'Song 2',
        type: FeedType.Song,
        image: 'https://via.placeholder.com/300x200',
      },
      {
        id: '4',
        name: 'Album 2',
        type: FeedType.Album,
        image: 'https://via.placeholder.com/300x200',
      },
    ];

    return of(mockFeed);
  }
}
