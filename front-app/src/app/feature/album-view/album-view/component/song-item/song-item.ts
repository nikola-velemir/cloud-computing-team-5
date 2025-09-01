import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { loadTrack } from '../../../../content-audio-player/state/audio.actions';
import { AppState } from '../../../../../state/app-state';

@Component({
  selector: 'album-view-song-item',
  standalone: false,
  templateUrl: './song-item.html',
  styleUrl: './song-item.scss',
})
export class SongItem {
  constructor(private store: Store<AppState>) {}

  playSong() {
    this.store.dispatch(loadTrack({ trackId: '1' }));
  }
}
