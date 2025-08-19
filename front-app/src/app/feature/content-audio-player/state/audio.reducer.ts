import {Track} from '../model/track';
import {createReducer, on} from '@ngrx/store';
import {
  audioSeek, loadAlbum, loadAlbumSuccess,
  loadTrack,
  loadTrackFailure,
  loadTrackSuccess, nextTrack,
  pauseAudio,
  play,
  playTrackAtIndex, previousTrack,
  resumeAudio,
  stopAudio,
  trackFinished, trackProgress, volumeChange
} from './audio.actions';

export interface AudioPlayerState {
  isPlaying: boolean;
  loading: boolean;
  error: string | null;
  currentTime: number;
  duration: number;
  volume: number;
  currentTrackIndex: number | null,
  playList: Track[],
}


export const initialState: AudioPlayerState = {
  isPlaying: false,
  loading: true,
  error: null,
  currentTime: 0,
  duration: 0,
  volume: 0.5,
  currentTrackIndex: null,
  playList: []
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
    playList: [track],
    currentTrackIndex: 0,
    loading: false,
    isPlaying: true,
  })),
  on(loadTrackFailure, (state, {error}) => ({
    ...state,
    error: error,
  })),
  on(nextTrack, (state) => ({
    ...state,
  })),
  on(previousTrack, (state) => ({
    ...state,
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
      currentTrackIndex: null,
      isPlaying: false,
    }
  }),
  on(trackFinished, (state, {track}) => {
    const index = state.playList.findIndex(t => track.id === t.id);
    return {
      ...state,
      currentTrackIndex: index,
      isPlaying: false,
    }
  }),
  on(resumeAudio, (state) => {
    console.log(state);
    return {
      ...state,
      isPlaying: true,
    }
  }),
  on(trackProgress, (state, {currentTime, duration}) => ({
    ...state,
    currentTime: currentTime,
    duration: duration,
  })),
  on(audioSeek, (state, {newDuration}) => ({
    ...state,
    currentTime: newDuration,
  })),
  on(volumeChange, (state, {volume}) => ({
    ...state,
    volume: volume,
  })),
  on(playTrackAtIndex, (state, {index}) => {
    console.log(state);
    return {
      ...state,
      currentTrackIndex: index,
    }
  }),
  on(loadAlbum, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),

  on(loadAlbumSuccess, (state, {album}) => ({
    ...state,
    playList: [...album.tracks],
    currentTrackIndex: 0,
    loading: false,
    isPlaying: true,
  })),
  on(nextTrack, (state) => ({
    ...state
  }))
)

