import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {AudioApi} from '../service/audio-api.service';
import {
  audioSeek, loadAlbum, loadAlbumFailure, loadAlbumSuccess,
  loadTrack,
  loadTrackFailure,
  loadTrackSuccess, nextTrack,
  pauseAudio,
  play, playTrackAtIndex, previousTrack,
  resumeAudio,
  stopAudio,
  trackFinished, volumeChange
} from './audio.actions';
import {catchError, map, of, switchMap, tap, withLatestFrom} from 'rxjs';
import {AudioService} from '../service/audio-service';
import {createAction, Store} from '@ngrx/store';
import {AppState} from '../../../state/app-state';
import {selectCurrentPlaylistAndIndex, selectCurrentTime, selectPlaylist} from './audio.selectors';

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

  constructor(private actions$: Actions, private api: AudioApi, private audioService: AudioService, private store: Store<AppState>) {
    this.loadTrack$ = createEffect(() =>
      this.actions$.pipe(
        ofType(loadTrack),
        switchMap(({trackId}) =>
          this.api.getTrack(trackId).pipe(
            map((track) => {
              console.log(track);
              return loadTrackSuccess({track})
            }),
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
          tap((t) => {
            console.log(t)
            return store.dispatch(play(t))
          })),
      {dispatch: false});
    this.loadAlbum$ = createEffect(() =>
      this.actions$.pipe(
        ofType(loadAlbum),
        switchMap(({albumId}) =>
          this.api.getAlbum(albumId).pipe(tap((a) => console.log(a)),
            map(album => loadAlbumSuccess({album})),
            catchError(err =>
              of(loadAlbumFailure({error: err.message || 'Failed to load album'}))
            )
          )
        )
      )
    )
    ;
    this.loadAlbumSuccess$ = createEffect(() =>
      this.actions$.pipe(
        ofType(loadAlbumSuccess),
        tap((a) => {
          console.log(a);
          return store.dispatch(play({track: a.album.tracks[0]}))
        })
      ), {dispatch: false})

    this.playTrack$ = createEffect(() =>
      this.actions$.pipe(
        ofType(play),
        tap(({track}
        ) => {
          this.store.select(selectPlaylist).subscribe(playList => {
            const index = playList.findIndex(t => t.id === track.id);
            if (index !== -1) {
              this.store.dispatch(playTrackAtIndex({index}))
            }
          }).unsubscribe();
          if (track.url) {
            this.audioService.stop();
            this.audioService.play(track.url);
          }
        })), {dispatch: false});

    this.pauseTrack$ = createEffect(() =>
      this.actions$.pipe(ofType(pauseAudio),
        tap(() => {
          this.audioService.pause();
        })), {dispatch: false});
    this.trackFinished$ = createEffect(() => this.actions$.pipe(
      ofType(trackFinished),
      withLatestFrom(this.store.select(selectPlaylist)),
      tap(([{track}, playList]) => {
        console.log(playList)
        const index = playList.findIndex(t => t.id === track.id);
        if (index !== -1 && index + 1 < playList.length) {
          this.store.dispatch(nextTrack());
        } else {
          this.store.dispatch(stopAudio());
        }
      })
    ), {dispatch: false});
    this.resumeTrack$ = createEffect(() => this.actions$.pipe(ofType(resumeAudio),
      tap(() => {
        this.audioService.resume();
      })), {dispatch: false});

    this.stopTrack$ = createEffect(() => this.actions$.pipe(ofType(stopAudio),
      tap(() => {
        console.log('AA')
        this.audioService.stop();
      })), {dispatch: false});

    this.audioSeek$ = createEffect(() => this.actions$.pipe(ofType(audioSeek),
      tap(({newDuration}) => this.audioService.seek(newDuration))), {dispatch: false})

    this.volumeChange$ = createEffect(() => this.actions$.pipe(ofType(volumeChange),
      tap(({volume}) => this.audioService.changeVolume(volume))), {dispatch: false});

    this.previousTrack$ = createEffect(() => this.actions$.pipe(ofType(previousTrack),
      withLatestFrom(this.store.select(selectCurrentPlaylistAndIndex), this.store.select(selectCurrentTime)),
      tap(([, {currentTrackIndex, playList}, time]) => {
        if ( time > 2) {
          this.store.dispatch(play({track: playList[currentTrackIndex !== null ? currentTrackIndex : 0]}))
          return;
        }
        if (currentTrackIndex === null) {
          this.store.dispatch(play({track: playList[0]}))
          return;
        }
        const previousIndex = currentTrackIndex - 1;
        if (previousIndex < 0) {
          this.store.dispatch(play({track: playList[0]}))
          return;
        }
        this.store.dispatch(play({track: playList[previousIndex]}))
      })
    ), {dispatch: false});

    this.nextTrack$ = createEffect(() => this.actions$.pipe(ofType(nextTrack),
      withLatestFrom(this.store.select(selectCurrentPlaylistAndIndex)),
      tap(([_, {currentTrackIndex, playList}]) => {
        console.log("AAA")
        console.log(currentTrackIndex)
        console.log(playList)
        if (currentTrackIndex === null) {
          this.store.dispatch(stopAudio())
          return;
        }
        const nextIndex = currentTrackIndex + 1;
        if (nextIndex >= playList.length) {
          this.store.dispatch(stopAudio())
          return;
        }
        this.store.dispatch(play({track: playList[nextIndex]}));

      })), {dispatch: false});
  }
}
