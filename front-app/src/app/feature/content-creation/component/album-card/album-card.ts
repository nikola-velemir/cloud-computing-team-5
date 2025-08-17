import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Album} from '../../model/album';

@Component({
  selector: 'app-album-card',
  standalone:false,
  templateUrl: './album-card.html',
  styleUrl: './album-card.scss'
})
export class AlbumCard {
  @Input() album!: Album;
  @Output() onSelect = new EventEmitter<Album>();

}
