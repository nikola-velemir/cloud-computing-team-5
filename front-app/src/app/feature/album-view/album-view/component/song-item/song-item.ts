import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import { loadTrack } from '../../../../content-audio-player/state/audio.actions';
import { AppState } from '../../../../../state/app-state';
import { AlbumViewSongResponse } from '../../../model/album-view-song-response';

@Component({
  selector: 'album-view-song-item',
  standalone: false,
  templateUrl: './song-item.html',
  styleUrl: './song-item.scss',
})
export class SongItem {
  @Input() song: AlbumViewSongResponse | null = null;
  constructor(private store: Store<AppState>) {}

  playSong() {
    if (!this.song) return;
    this.store.dispatch(loadTrack({ trackId: this.song.id }));
  }
}
