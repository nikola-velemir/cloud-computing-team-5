import { Component, Input } from '@angular/core';
import { HomeGenre } from '../../model/home-genre.model';

@Component({
  selector: 'app-home-genre-card',
  standalone: false,
  templateUrl: './home-genre-card.html',
  styleUrl: './home-genre-card.scss',
})
export class HomeGenreCard {
  @Input()
  genre!: HomeGenre;
}
