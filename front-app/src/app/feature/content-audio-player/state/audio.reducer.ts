import { Track } from '../model/track';
import { createReducer, on } from '@ngrx/store';
import {
  audioSeek,
  loadAlbum,
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
  trackCachedSuccess,
  trackFinished,
  trackProgress,
  volumeChange,
} from './audio.actions';

export interface AudioPlayerState {
  cachedTrackIds: any;
  isPlaying: boolean;
  loading: boolean;
  error: string | null;
  currentTime: number;
  duration: number;
  volume: number;
  currentTrack: Track | null;
  playList: string[];
}

export const initialState: AudioPlayerState = {
  isPlaying: false,
  loading: true,
  error: null,
  currentTime: 0,
  duration: 0,
  volume: 0.5,
  currentTrack: null,
  playList: [],
  cachedTrackIds: [],
};

export const audioPlayerReducer = createReducer(
  initialState,
  on(loadTrack, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),
  on(loadTrackSuccess, (state, { track }) => {
    if (state.playList.length > 0)
      return {
        ...state,
        currentTrack: { ...track },
        loading: false,
        isPlaying: true,
        duration: track.duration,
      };
    return {
      ...state,
      playList: [track.id],
      currentTrack: { ...track },
      loading: false,
      isPlaying: true,
      duration: track.duration,
    };
  }),
  on(loadTrackFailure, (state, { error }) => ({
    ...state,
    error: error,
  })),
  on(nextTrack, (state) => ({
    ...state,
  })),
  on(previousTrack, (state) => ({
    ...state,
  })),
  on(play, (state) => ({
    ...state,
    isPlaying: true,
  })),
  on(pauseAudio, (state) => ({
    ...state,
    isPlaying: false,
  })),
  on(stopAudio, (state) => ({
    ...state,
    currentTrack: null,
    playList: [],
    isPlaying: false,
  })),
  on(trackFinished, (state, { track }) => {
    return {
      ...state,
      isPlaying: false,
    };
  }),
  on(resumeAudio, (state) => ({
    ...state,
    isPlaying: true,
  })),
  on(trackProgress, (state, { currentTime }) => ({
    ...state,
    currentTime: currentTime,
  })),
  on(audioSeek, (state, { newDuration }) => ({
    ...state,
    currentTime: newDuration,
  })),
  on(volumeChange, (state, { volume }) => ({
    ...state,
    volume: volume,
  })),
  on(loadAlbum, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),

  on(loadAlbumSuccess, (state, { album }) => ({
    ...state,
    playList: [...album.tracks],
    loading: false,
    isPlaying: true,
  })),
  on(nextTrack, (state) => ({
    ...state,
  })),
  on(trackCachedSuccess, (state, { trackId }) => ({
    ...state,
    cachedTrackIds: [...state.cachedTrackIds, trackId],
  }))
);
