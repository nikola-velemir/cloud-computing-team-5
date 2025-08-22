import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Author } from '../../../model/author';

@Component({
  selector: 'app-author-card',
  standalone: false,
  templateUrl: './author-card.html',
  styleUrl: './author-card.scss',
})
export class AuthorCard {
  @Input() author!: Author;
  checked = false;
  @Output() onSelect = new EventEmitter<Author>();

  select() {
    console.log(this.author);
    this.onSelect.emit(this.author);
  }
}
