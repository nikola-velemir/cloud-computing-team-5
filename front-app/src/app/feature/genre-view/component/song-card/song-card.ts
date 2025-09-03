import { Component } from '@angular/core';
import { AppState } from '../../../../state/app-state';
import { Store } from '@ngrx/store';
import {
  loadTrack,
  play,
} from '../../../content-audio-player/state/audio.actions';

@Component({
  selector: 'genre-view-song-card',
  imports: [],
  templateUrl: './song-card.html',
  styleUrl: './song-card.scss',
})
export class SongCard {
  constructor(private store: Store<AppState>) {}

  playSong() {
    this.store.dispatch(loadTrack({ trackId: '2' }));
  }
}
