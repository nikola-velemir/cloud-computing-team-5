import { Component, Input } from '@angular/core';
import { Song } from '../../model/song.model';

@Component({
  selector: 'app-song-card',
  standalone: false,
  templateUrl: './song-card.html',
  styleUrl: './song-card.scss',
})
export class SongCard {
  @Input()
  song!: Song;

  constructor() {}
}
