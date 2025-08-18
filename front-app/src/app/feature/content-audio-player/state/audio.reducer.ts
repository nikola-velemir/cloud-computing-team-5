import {Track} from '../model/track';
import {createReducer, on} from '@ngrx/store';
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
import {state} from '@angular/animations';
import {retry} from 'rxjs';

export interface AudioPlayerState {
  isPlaying: boolean;
  currentTrack: Track | null;
  loading: boolean;
  error: string | null;
}


export const initialState: AudioPlayerState = {
  isPlaying: false,
  currentTrack: null,
  loading: true,
  error: null,
}

export const audioPlayerReducer = createReducer(
  initialState,
  on(loadTrack, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),
  on(loadTrackSuccess, (state, {track}) => ({
    ...state,
    currentTrack: track,
    loading: false,
    isPlaying: true,
  })),
  on(loadTrackFailure, (state, {error}) => ({
    ...state,
    error: error,
  })),
  on(play, (state,) => ({
    ...state,
    isPlaying: true,
  })),
  on(pauseAudio, (state) => ({
    ...state,
    isPlaying: false,
  })),
  on(stopAudio, (state) => {
    console.log(state);
    return {
      ...state,
      currentTrack: null,
      isPlaying: false,
    }
  }),
  on(trackFinished, (state, {track}) => ({
    ...state,
    track: track,
    isPlaying: false,
  })),
  on(resumeAudio, (state) => {
    console.log(state);
    return {
      ...state,
      isPlaying: true,
    }
  })
)
