import {Component} from '@angular/core';
import {Store} from '@ngrx/store';
import {AppState} from '../../../../../state/app-state';
import {loadAlbum} from '../../../../content-audio-player/state/audio.actions';

@Component({
  selector: 'app-album.ts-view',
  standalone: false,
  templateUrl: './album-view.html',
  styleUrl: './album-view.scss'
})
export class AlbumView {
  constructor(private store: Store<AppState>) {
  }

  playAlbum() {
    this.store.dispatch(loadAlbum({albumId: 1}))
  }
}
