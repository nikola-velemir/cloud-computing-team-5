import { Component, Input } from '@angular/core';
import { HomeArtist } from '../../model/home-artist.model';

@Component({
  selector: 'app-home-artist-card',
  standalone: false,
  templateUrl: './home-artist-card.html',
  styleUrl: './home-artist-card.scss',
})
export class HomeArtistCard {
  @Input()
  artist!: HomeArtist;
}
