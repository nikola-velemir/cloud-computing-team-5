import {Component, OnDestroy, OnInit} from '@angular/core';
import {Observable, of, Subscription} from 'rxjs';
import {Track} from '../../model/track';
import {AppState} from '../../../../state/app-state';
import {Store} from '@ngrx/store';
import {selectCurrentTrack, selectIsPlaying} from '../../state/audio.selectors';
import {AsyncPipe, NgClass, NgIf} from '@angular/common';
import {pauseAudio, resumeAudio, stopAudio} from '../../state/audio.actions';

@Component({
  selector: 'app-audio-player',
  imports: [
    NgIf,
    AsyncPipe,
    NgClass
  ],
  templateUrl: './audio-player.html',
  styleUrl: './audio-player.scss'
})
export class AudioPlayer implements OnInit, OnDestroy {
  currentTrack$: Observable<Track | null> = of(null);
  isPlaying$: Observable<boolean> = of(false);
  currentTrackSub: Subscription | null = null;
  isPlayingSub: Subscription | null = null;

  constructor(private store: Store<AppState>) {
    this.currentTrack$ = this.store.select(selectCurrentTrack);
    this.isPlaying$ = this.store.select(selectIsPlaying);
  }

  ngOnInit(): void {
    this.currentTrackSub = this.currentTrack$.subscribe(track => console.log(track));
    this.isPlayingSub = this.isPlaying$.subscribe(isPlaying => console.log(isPlaying));
  }

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
}
