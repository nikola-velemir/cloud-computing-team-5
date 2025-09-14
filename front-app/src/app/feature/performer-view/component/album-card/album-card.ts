import { Component, Input } from '@angular/core';
import { AritstViewAlbumResponse } from '../../model/artist-view-album-response';

@Component({
  selector: 'performer-view-album-card',
  standalone: false,
  templateUrl: './album-card.html',
  styleUrl: './album-card.scss',
})
export class AlbumCard {
  @Input() album: AritstViewAlbumResponse | null = null;
}
