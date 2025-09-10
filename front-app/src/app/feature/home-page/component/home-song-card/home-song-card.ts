import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { loadTrack } from '../../../content-audio-player/state/audio.actions';
import { HomeSong } from '../../model/home-song.mode';

@Component({
  selector: 'app-home-song-card',
  standalone: false,
  templateUrl: './home-song-card.html',
  styleUrl: './home-song-card.scss',
})
export class HomeSongCard {
  @Input()
  song!: HomeSong;
  @ViewChild('audioPlayer') audioPlayer!: ElementRef<HTMLAudioElement>;

  constructor(private store: Store<AppState>) {}

  playSong() {
    this.store.dispatch(loadTrack({ trackId: this.song?.id ?? '' }));
  }
}
