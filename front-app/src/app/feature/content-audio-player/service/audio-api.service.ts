import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {Track} from '../model/track';
import {Album} from '../model/album';

@Injectable({
  providedIn: 'root'
})
export class AudioApi {

  constructor() {
  }

  getTrack(trackId: number) {
    return of({
      id: trackId, name: 'Za beograd', performerName: 'Firma Krstic',
      url: '/audio/ccokolada.mp3', duration: 30
    } as Track)
  }

  getAlbum(albumId: number): Observable<Album> {
    const album: Album = {
      id: 1,
      tracks: [
        {id: 2, name: "Rendalicca", performerName: 'Desingerica', url: '/audio/rendalicca.mp3', duration: 30}, {
          id: 1, name: 'Za beograd', performerName: 'Firma Krstic',
          url: '/audio/ccokolada.mp3', duration: 30
        },]
    }
    return of(album);
  }
}
