import {createAction, props} from '@ngrx/store';
import {Track} from '../model/track';
import {strict} from 'node:assert';

export const play = createAction(
  '[AudioService Player] Play',
  props<{ track: Track }>()
)

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
