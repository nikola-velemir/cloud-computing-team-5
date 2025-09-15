import { Component, Input } from '@angular/core';
import { SongViewAlbumResponse } from '../../model/song-view-album-response';

@Component({
  selector: 'song-view-album-card',
  standalone: false,
  templateUrl: './album-card.html',
  styleUrl: './album-card.scss',
})
export class AlbumCard {
  @Input() album: SongViewAlbumResponse | null = null;
}
