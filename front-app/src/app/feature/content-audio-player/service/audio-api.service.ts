import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {Track} from '../model/track';
import {AlbumMetadata} from '../model/album';

@Injectable({
  providedIn: 'root'
})
export class AudioApi {

  constructor() {
  }

  getTrack(trackId: number) {
    if (trackId == 2) {
      return of({
        id: trackId, name: 'Za beograd', performerName: 'Firma Krstic',
        url: '/audio/ccokolada.mp3', duration: 30
      } as Track)
    }
    return of({
      id: trackId, name: 'Rendalicca', performerName: 'Desingerica',
      url: '/audio/rendalicca.mp3', duration: 30
    } as Track)

  }

  getAlbum(albumId: number): Observable<AlbumMetadata> {
    const album: AlbumMetadata = {
      id: 1,
      tracks: [2, 3]
    }
    return of(album);
  }
}
