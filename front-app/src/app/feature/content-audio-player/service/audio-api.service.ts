import {Injectable} from '@angular/core';
import {of} from 'rxjs';
import {Track} from '../model/track';

@Injectable({
  providedIn: 'root'
})
export class AudioApi {

  constructor() {
  }

  getTrack(trackId: number) {
    return of({
      id: trackId, name: 'Za beograd', performerName: 'Firma Krstic',
      url: '/audio/my-song.mp3'
    } as Track)
  }
}
