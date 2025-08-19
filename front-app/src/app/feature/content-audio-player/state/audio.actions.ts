import {createAction, props} from '@ngrx/store';
import {Track} from '../model/track';
import {strict} from 'node:assert';
import {Album} from '../model/album';

export const play = createAction(
  '[AudioService Player] Play',
  props<{ track: Track }>()
)
export const trackProgress = createAction('[AudioService Player] Track Progress', props<{
  currentTime: number,
  duration: number
}>());
export const audioSeek = createAction('[AudioService Player] Audio Seek', props<{ newDuration: number }>());

export const pauseAudio = createAction('[AudioService Player] Pause')
export const resumeAudio = createAction('[AudioService Player] Resume')
export const stopAudio = createAction('[AudioService Player] Stop')
export const loadTrack = createAction('[AudioService Player] Load Track', props<{ trackId: number }>())
export const loadTrackSuccess = createAction('[AudioService Player] Load Track Success', props<{ track: Track }>())
export const loadTrackFailure = createAction('[AudioService Player] Load Track Failure', props<{ error: string }>())
export const trackFinished = createAction(
  '[AudioService Player] Track Finished',
  props<{ track: Track }>()
);
export const playTrackAtIndex = createAction(
  '[AudioService Player] Play Track At Index',
  props<{ index: number }>()
);

export const nextTrack = createAction('[AudioService Player] Next Track');
export const previousTrack = createAction('[AudioService Player] Previous Track');
export const addTrackToPlaylist = createAction('[Audio Service] Add Track To Playlist', props<{ track: Track }>());
export const volumeChange = createAction('[AudioService Player] Volume Change', props<{ volume: number }>());
export const loadAlbum = createAction('[AudioService Player] Load Album', props<{ albumId: number }>());
export const loadAlbumSuccess = createAction('[AudioService Plater] Load Album Success', props<{ album: Album }>());
export const loadAlbumFailure = createAction('[AudioService Player] Load Album Failure', props<{ error: string }>())
