import { Component, Input } from '@angular/core';
import { GenreArtistPreviewResponse } from '../../model/model';

@Component({
  selector: 'genre-view-performer-card',
  standalone: false,
  templateUrl: './performer-card.html',
  styleUrl: './performer-card.scss',
})
export class PerformerCard {
  @Input() artist: GenreArtistPreviewResponse | null = null;
}
