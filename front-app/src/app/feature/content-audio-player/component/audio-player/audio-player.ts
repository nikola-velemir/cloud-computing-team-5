import { Component, OnDestroy, OnInit } from '@angular/core';
import { Observable, of, Subscription } from 'rxjs';
import { Track } from '../../model/track';
import { AppState } from '../../../../state/app-state';
import { Store } from '@ngrx/store';
import {
  currentVolume,
  selectCurrentTime,
  selectCurrentTrack,
  selectDuration,
  selectIsPlaying,
} from '../../state/audio.selectors';
import {
  audioSeek,
  nextTrack,
  pauseAudio,
  previousTrack,
  resumeAudio,
  stopAudio,
  volumeChange,
} from '../../state/audio.actions';

@Component({
  selector: 'app-audio-player',
  standalone: false,
  templateUrl: './audio-player.html',
  styleUrl: './audio-player.scss',
})
export class AudioPlayer implements OnInit, OnDestroy {
  currentTrack$: Observable<Track | null> = of(null);
  isPlaying$: Observable<boolean> = of(false);
  currentTrackSub: Subscription | null = null;
  isPlayingSub: Subscription | null = null;
  currentTime$: Observable<number>;
  duration$: Observable<number>;

  soundSettingsOpen: boolean = false;
  volume$: Observable<number>;

  constructor(private store: Store<AppState>) {
    this.currentTrack$ = this.store.select(selectCurrentTrack);
    this.isPlaying$ = this.store.select(selectIsPlaying);
    this.currentTime$ = this.store.select(selectCurrentTime);
    this.duration$ = this.store.select(selectDuration);
    this.volume$ = this.store.select(currentVolume);
  }

  ngOnInit(): void {}

  ngOnDestroy(): void {
    this.currentTrackSub?.unsubscribe();
    this.isPlayingSub?.unsubscribe();
  }

  stopAudio() {
    this.store.dispatch(stopAudio());
  }

  pauseAudio() {
    this.store.dispatch(pauseAudio());
  }

  resumeAudio() {
    this.store.dispatch(resumeAudio());
  }

  onSeek($event: any) {
    const inputElement = $event.target as HTMLInputElement;
    const value = Number(inputElement.value);
    if (isNaN(value)) return;
    this.store.dispatch(audioSeek({ newDuration: value }));
  }

  toggleSoundSettings() {
    this.soundSettingsOpen = !this.soundSettingsOpen;
  }

  volumeChange($event: Event) {
    const inputElement = $event.target as HTMLInputElement;
    const volume = Number(inputElement.value);
    if (isNaN(volume)) return;
    this.store.dispatch(volumeChange({ volume }));
  }

  forward() {
    this.store.dispatch(nextTrack());
  }
  backward() {
    this.store.dispatch(previousTrack());
  }
}
