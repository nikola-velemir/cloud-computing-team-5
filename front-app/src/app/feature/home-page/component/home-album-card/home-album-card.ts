import { Component, Input } from '@angular/core';
import { HomeAlbum } from '../../model/home-album.model';

@Component({
  selector: 'app-home-album-card',
  standalone: false,
  templateUrl: './home-album-card.html',
  styleUrl: './home-album-card.scss',
})
export class HomeAlbumCard {
  @Input()
  album!: HomeAlbum;
}
