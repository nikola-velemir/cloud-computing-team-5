import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { loadTrack } from '../../../content-audio-player/state/audio.actions';

@Component({
  selector: 'performer-view-song-item',
  standalone: false,
  templateUrl: './song-item.html',
  styleUrl: './song-item.scss',
})
export class SongItem {
  private songId = 'aa';

  constructor(private store: Store<AppState>) {}

  playSong() {
    this.store.dispatch(loadTrack({ trackId: this.songId }));
  }
}
