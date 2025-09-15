import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { loadTrack } from '../../../content-audio-player/state/audio.actions';
import { GenreSongPreviewResponse } from '../../model/model';

@Component({
  selector: 'genre-view-song-card',
  templateUrl: './song-card.html',
  standalone: false,
  styleUrl: './song-card.scss',
})
export class SongCard {
  @Input() song: GenreSongPreviewResponse | null = null;

  constructor(private store: Store<AppState>) {}

  playSong() {
    if (!this.song) return;
    this.store.dispatch(loadTrack({ trackId: this.song.id }));
  }
}
