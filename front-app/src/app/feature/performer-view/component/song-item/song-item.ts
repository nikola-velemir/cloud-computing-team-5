import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { loadTrack } from '../../../content-audio-player/state/audio.actions';
import { ArtistViewSongResponse } from '../../model/artist-view-song-response';

@Component({
  selector: 'performer-view-song-item',
  standalone: false,
  templateUrl: './song-item.html',
  styleUrl: './song-item.scss',
})
export class SongItem {
  @Input() song: ArtistViewSongResponse | null = null;

  constructor(private store: Store<AppState>) {}

  playSong() {
    if (this.song) this.store.dispatch(loadTrack({ trackId: this.song.id }));
  }
}
