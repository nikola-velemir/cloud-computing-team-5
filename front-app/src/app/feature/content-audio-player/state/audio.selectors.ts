import {createSelector} from '@ngrx/store';
import {AppState} from '../../../state/app-state';
import {AudioPlayerState} from './audio.reducer';

export const trackState = (state: AppState) => state.audio;
export const selectCurrentTrack = createSelector(
  trackState,
  (state: AudioPlayerState) => state.currentTrack
)
export const selectIsPlaying = createSelector(
  trackState,
  (state: AudioPlayerState) => state.isPlaying
)
