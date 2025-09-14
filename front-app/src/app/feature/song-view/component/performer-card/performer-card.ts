import { Component, Input } from '@angular/core';
import { SongViewArtistResponse } from '../../model/song-view-artist-response';

@Component({
  selector: 'song-view-performer-card',
  standalone: false,
  templateUrl: './performer-card.html',
  styleUrl: './performer-card.scss',
})
export class PerformerCard {
  @Input() artist: SongViewArtistResponse | null = null;
}
