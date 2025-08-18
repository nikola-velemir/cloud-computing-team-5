import {Injectable} from '@angular/core';
import {Howl} from 'howler';
import {stopAudio, trackFinished} from '../state/audio.actions';
import {AppState} from '../../../state/app-state';
import {Store} from '@ngrx/store';
import {Track} from '../model/track';

@Injectable({
  providedIn: 'root'
})
export class AudioService {
  private sound: Howl | null = null;
  private currentTrack: Track | null = null;

  constructor(private store: Store<AppState>) {
  }

  play(url: string) {
    if (!this.sound) {
      this.sound = new Howl({
        src: [url],
        html5: true,
        onend: () => {
          if (this.currentTrack) {
            this.store.dispatch(trackFinished({ track: this.currentTrack }));
            this.currentTrack = null;
          }
        }
      })
    }
    this.sound.play();
  }

  pause() {
    this.sound?.pause();
  }

  stop() {
    this.sound?.stop();
    this.sound = null;
  }

  resume() {
    if (this.sound) {
      this.sound.play();
    }
  }
}
