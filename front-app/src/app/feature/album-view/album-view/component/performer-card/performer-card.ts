import { Component, Input } from '@angular/core';
import { AlbumViewArtistResponse } from '../../../model/album-view-artist-response';

@Component({
  selector: 'album-view-performer-card',
  standalone: false,
  templateUrl: './performer-card.html',
  styleUrl: './performer-card.scss',
})
export class PerformerCard {
  @Input() artist: AlbumViewArtistResponse | null = null;
}
