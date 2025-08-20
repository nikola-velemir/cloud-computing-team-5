import {Component, OnInit} from '@angular/core';
import {Store} from '@ngrx/store';
import {AppState} from '../../../../state/app-state';
import {loadTrack} from '../../../content-audio-player/state/audio.actions';
import {selectCurrentTrack} from '../../../content-audio-player/state/audio.selectors';

@Component({
  selector: 'song-view',
  standalone: false,
  templateUrl: './song-view.html',
  styleUrl: './song-view.scss'
})
export class SongView implements OnInit {
  constructor(private store: Store<AppState>) {
  }

  ngOnInit(): void {
  }


  playSong() {
    this.store.dispatch(loadTrack({trackId: 10}))
  }
}
