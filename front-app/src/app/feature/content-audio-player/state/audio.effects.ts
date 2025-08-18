import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {AudioApi} from '../service/audio-api.service';
import {
  loadTrack,
  loadTrackFailure,
  loadTrackSuccess,
  pauseAudio,
  play,
  resumeAudio,
  stopAudio,
  trackFinished
} from './audio.actions';
import {catchError, map, of, switchMap, tap} from 'rxjs';
import {AudioService} from '../service/audio-service';
import {Store} from '@ngrx/store';
import {AppState} from '../../../state/app-state';

@Injectable()
export class AudioPlayerEffects {
  loadTrack$;
  playTrack$;
  loadTrackSuccess$;
  pauseTrack$;
  resumeTrack$;
  stopTrack$;
  trackFinished$;

  constructor(private actions$: Actions, private api: AudioApi, private audioService: AudioService, private store: Store<AppState>) {
    this.loadTrack$ = createEffect(() =>
      this.actions$.pipe(
        ofType(loadTrack),
        switchMap(({trackId}) =>
          this.api.getTrack(trackId).pipe(
            map((track) => loadTrackSuccess({track})),
            catchError((err) =>
              of(loadTrackFailure({error: err.message || 'Failed to load track'}))
            )
          )
        )
      )
    );
    this.loadTrackSuccess$ = createEffect(() =>
        this.actions$.pipe(
          ofType(loadTrackSuccess),
          tap((t) => store.dispatch(play(t)))),
      {dispatch: false});
    this.playTrack$ = createEffect(() =>
      this.actions$.pipe(
        ofType(play),
        tap(({track}
        ) => {
          if (track.url) {
            this.audioService.play(track.url);
          }
        })), {dispatch: false});

    this.pauseTrack$ = createEffect(() =>
      this.actions$.pipe(ofType(pauseAudio),
        tap(() => {
          this.audioService.pause();
        })), {dispatch: false});
    this.trackFinished$ = createEffect(() => this.actions$.pipe(ofType(trackFinished), tap(() => {
      this.audioService.pause()
    })), {dispatch: false});
    this.resumeTrack$ = createEffect(() => this.actions$.pipe(ofType(resumeAudio),
      tap(() => {
        this.audioService.resume();
      })), {dispatch: false});

    this.stopTrack$ = createEffect(() => this.actions$.pipe(ofType(stopAudio),
      tap(() => {
        this.audioService.stop();
      })), {dispatch: false});
  }
}
