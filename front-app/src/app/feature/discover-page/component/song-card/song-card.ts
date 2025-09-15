import { Component, Input } from '@angular/core';
import { Song } from '../../model/song.model';
import { AppState } from '../../../../state/app-state';
import { Store } from '@ngrx/store';
import { loadTrack } from '../../../content-audio-player/state/audio.actions';

@Component({
  selector: 'app-song-card',
  standalone: false,
  templateUrl: './song-card.html',
  styleUrl: './song-card.scss',
})
export class SongCard {
  @Input()
  song!: Song;

  constructor(private store: Store<AppState>) {}

  playSong() {
    console.log(this.song);
    this.store.dispatch(loadTrack({ trackId: this.song?.Id ?? '' }));
  }
}
