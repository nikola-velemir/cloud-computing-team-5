import {createSelector} from '@ngrx/store';
import {AppState} from '../../../state/app-state';
import {AudioPlayerState} from './audio.reducer';
import {state} from '@angular/animations';

export const trackState = (state: AppState) => state.audio;
export const selectCurrentTrack = createSelector(
  trackState,
  (state: AudioPlayerState) => state.currentTrackIndex !== null ? state.playList[state.currentTrackIndex] : null
)
export const selectIsPlaying = createSelector(
  trackState,
  (state: AudioPlayerState) => state.isPlaying
)
export const selectPlaylist = createSelector(
  trackState,
  (state: AudioPlayerState) => state.playList
)
export const selectCurrentTrackIndex = createSelector(
  trackState,
  (state: AudioPlayerState) => state.currentTrackIndex
)
export const selectCurrentTime = createSelector(
  trackState,
  state => state.currentTime
)

export const selectDuration = createSelector(
  trackState,
  state => state.duration
)

export const selectCurrentPlaylistAndIndex = createSelector(
  trackState,
  state => ({currentTrackIndex: state.currentTrackIndex, playList: state.playList})
)

export const currentVolume = createSelector(
  trackState,
  state => state.volume
)
