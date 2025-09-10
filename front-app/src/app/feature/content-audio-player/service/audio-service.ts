import { Injectable } from '@angular/core';
import { Howl } from 'howler';
import {
  stopAudio,
  trackFinished,
  trackProgress,
  volumeChange,
} from '../state/audio.actions';
import { AppState } from '../../../state/app-state';
import { Store } from '@ngrx/store';
import { Track } from '../model/track';
import { interval, Observable, Subscription } from 'rxjs';
import { currentVolume, selectCurrentTrack } from '../state/audio.selectors';

@Injectable({
  providedIn: 'root',
})
export class AudioService {
  private sound: Howl | null = null;
  private currentTrack: Track | null = null;
  private currentTrack$;
  private prgoressSub: Subscription | null = null;
  private volume$;
  private volume = 0.5;

  constructor(private store: Store<AppState>) {
    this.volume$ = store.select(currentVolume);
    this.volume$.subscribe((v) => (this.volume = v));
    this.currentTrack$ = store.select(selectCurrentTrack);
    this.currentTrack$.subscribe((v) => (this.currentTrack = v));
  }

  play(url: string) {
    if (!this.sound) {
      this.sound = new Howl({
        src: [url],
        html5: true,
        volume: this.volume,
        onend: () => {
          if (this.currentTrack)
            this.store.dispatch(trackFinished({ track: this.currentTrack }));
        },
      });
    }
    this.sound.play();

    this.sound.once('load', () => {
      const duration = this.sound?.duration() ?? 0;
      this.prgoressSub = interval(500).subscribe(() => {
        if (this.sound) {
          this.store.dispatch(
            trackProgress({
              currentTime: Math.floor(this.sound.seek() as number),
            })
          );
        }
      });
    });
  }

  changeVolume(volume: number) {
    if (!this.sound) return;
    this.sound.volume(volume);
  }

  seek(value: number) {
    if (!this.sound) return;
    this.sound.seek(value);
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
