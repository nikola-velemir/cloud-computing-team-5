import { Component, Input } from '@angular/core';
import { GenreAlbumPreviewResponse } from '../../model/model';

@Component({
  selector: 'genre-view-album-card',
  standalone: false,
  templateUrl: './album-card.html',
  styleUrl: './album-card.scss',
})
export class AlbumCard {
  @Input() album: GenreAlbumPreviewResponse | null = null;
}
