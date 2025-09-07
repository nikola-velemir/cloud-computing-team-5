import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { AudioApi } from '../service/audio-api.service';
import {
  audioSeek,
  loadAlbum,
  loadAlbumFailure,
  loadAlbumSuccess,
  loadTrack,
  loadTrackFailure,
  loadTrackSuccess,
  nextTrack,
  pauseAudio,
  play,
  previousTrack,
  resumeAudio,
  stopAudio,
  trackFinished,
  volumeChange,
} from './audio.actions';
import { catchError, map, of, switchMap, tap, withLatestFrom } from 'rxjs';
import { AudioService } from '../service/audio-service';
import { Store } from '@ngrx/store';
import { AppState } from '../../../state/app-state';
import {
  selectCurrentPlaylistAndTrack,
  selectCurrentTime,
  selectPlaylist,
} from './audio.selectors';

@Injectable()
export class AudioPlayerEffects {
  loadTrack$;
  playTrack$;
  loadTrackSuccess$;
  pauseTrack$;
  resumeTrack$;
  stopTrack$;
  trackFinished$;
  audioSeek$;
  volumeChange$;
  loadAlbum$;
  loadAlbumSuccess$;
  nextTrack$;
  previousTrack$;

  constructor(
    private actions$: Actions,
    private api: AudioApi,
    private audioService: AudioService,
    private store: Store<AppState>
  ) {
    this.loadTrack$ = createEffect(() =>
      this.actions$.pipe(
        ofType(loadTrack),
        switchMap(({ trackId }) =>
          this.api.getTrack(trackId).pipe(
            map((track) => loadTrackSuccess({ track })),
            catchError((err) =>
              of(
                loadTrackFailure({
                  error: err.message || 'Failed to load track',
                })
              )
            )
          )
        )
      )
    );
    this.loadTrackSuccess$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(loadTrackSuccess),
          tap((t) => {
            console.log(t);
            return store.dispatch(play(t));
          })
        ),
      { dispatch: false }
    );
    this.loadAlbum$ = createEffect(() =>
      this.actions$.pipe(
        ofType(loadAlbum),
        switchMap(({ albumId }) =>
          this.api.getAlbum(albumId).pipe(
            map((album) => loadAlbumSuccess({ album })),
            catchError((err) =>
              of(
                loadAlbumFailure({
                  error: err.message || 'Failed to load album',
                })
              )
            )
          )
        )
      )
    );
    this.loadAlbumSuccess$ = createEffect(() =>
      this.actions$.pipe(
        ofType(loadAlbumSuccess),
        map(({ album }) => loadTrack({ trackId: album.tracks[0] }))
      )
    );

    this.playTrack$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(play),
          withLatestFrom(this.store.select(selectPlaylist)),
          tap(([{ track }, playList]) => {
            const index = playList.findIndex((t) => t === track.id);
            console.log(track);
            if (track.audioUrl) {
              this.audioService.stop();
              this.audioService.play(track.audioUrl);
            }
          })
        ),
      { dispatch: false }
    );

    this.pauseTrack$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(pauseAudio),
          tap(() => {
            this.audioService.pause();
          })
        ),
      { dispatch: false }
    );
    this.trackFinished$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(trackFinished),
          withLatestFrom(this.store.select(selectPlaylist)),
          tap(([{ track }, playList]) => {
            const index = playList.findIndex((t) => t === track.id);
            if (index !== -1 && index + 1 < playList.length) {
              this.store.dispatch(nextTrack());
            } else {
              this.store.dispatch(stopAudio());
            }
          })
        ),
      { dispatch: false }
    );
    this.resumeTrack$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(resumeAudio),
          tap(() => {
            this.audioService.resume();
          })
        ),
      { dispatch: false }
    );

    this.stopTrack$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(stopAudio),
          tap(() => {
            this.audioService.stop();
          })
        ),
      { dispatch: false }
    );

    this.audioSeek$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(audioSeek),
          tap(({ newDuration }) => this.audioService.seek(newDuration))
        ),
      { dispatch: false }
    );

    this.volumeChange$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(volumeChange),
          tap(({ volume }) => this.audioService.changeVolume(volume))
        ),
      { dispatch: false }
    );

    this.previousTrack$ = createEffect(
      () =>
        this.actions$.pipe(
          ofType(previousTrack),
          withLatestFrom(
            this.store.select(selectCurrentPlaylistAndTrack),
            this.store.select(selectCurrentTime)
          ),
          map(([, { currentTrack, playList }, time]) => {
            if (time > 2 && currentTrack !== null) {
              return this.store.dispatch(play({ track: currentTrack }));
            }
            if (currentTrack === null) {
              return this.store.dispatch(loadTrack({ trackId: playList[0] }));
            }
            const currentIndex = playList.findIndex(
              (t) => t === currentTrack.id
            );
            return currentIndex <= 0
              ? this.store.dispatch(loadTrack({ trackId: playList[0] }))
              : this.store.dispatch(
                  loadTrack({ trackId: playList[currentIndex - 1] })
                );
          })
        ),
      { dispatch: false }
    );

    this.nextTrack$ = createEffect(() =>
      this.actions$.pipe(
        ofType(nextTrack),
        withLatestFrom(this.store.select(selectCurrentPlaylistAndTrack)),
        map(([_, { currentTrack, playList }]) => {
          if (!currentTrack) {
            return stopAudio();
          }
          const currentTrackIndex = playList.findIndex(
            (t) => t === currentTrack.id
          );
          const nextIndex = currentTrackIndex + 1;
          return nextIndex < playList.length
            ? loadTrack({ trackId: playList[nextIndex] })
            : stopAudio();
        })
      )
    );
  }
}
