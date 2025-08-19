import {createSelector} from '@ngrx/store';
import {AppState} from '../../../state/app-state';
import {AudioPlayerState} from './audio.reducer';
import {state} from '@angular/animations';

export const trackState = (state: AppState) => state.audio;
export const selectCurrentTrack = createSelector(
  trackState,
  (state: AudioPlayerState) => state.currentTrack
)
export const selectIsPlaying = createSelector(
  trackState,
  (state: AudioPlayerState) => state.isPlaying
)
export const selectPlaylist = createSelector(
  trackState,
  (state: AudioPlayerState) => state.playList
)

export const selectCurrentTime = createSelector(
  trackState,
  state => state.currentTime
)

export const selectDuration = createSelector(
  trackState,
  state => state.duration
)

export const selectCurrentPlaylistAndTrack = createSelector(
  trackState,
  state => ({currentTrack: state.currentTrack, playList: state.playList})
)

export const currentVolume = createSelector(
  trackState,
  state => state.volume
)
