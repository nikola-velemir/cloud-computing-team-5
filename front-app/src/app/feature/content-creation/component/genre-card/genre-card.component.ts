import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Genre} from '../../model/genre';

@Component({
  selector: 'app-genre-card',
  standalone: false,
  templateUrl: './genre-card.component.html',
  styleUrl: './genre-card.component.scss'
})
export class GenreCard {
  @Input() genre!: Genre;
  @Output() onSelect = new EventEmitter();
  selectGenre() {
    this.onSelect.emit(this.genre);
  }
}
