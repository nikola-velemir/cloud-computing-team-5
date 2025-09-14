import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Artist } from '../../../model/artist';

@Component({
  selector: 'content-creation-artist-card',
  standalone: false,
  templateUrl: './artist-card.html',
  styleUrl: './artist-card.scss',
})
export class ArtistCard {
  @Input() author!: Artist;
  checked = false;
  @Output() onSelect = new EventEmitter<Artist>();

  select() {
    this.onSelect.emit(this.author);
  }
}
