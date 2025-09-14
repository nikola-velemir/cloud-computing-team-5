import { Component, OnInit } from '@angular/core';
import {
  ContentCreationService,
  SongData,
} from '../../../service/content-creation.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'content-creation-song-list',
  standalone: false,
  templateUrl: './song-list.html',
  styleUrl: './song-list.scss',
})
export class SongList implements OnInit {
  songs$!: Observable<SongData[]>;
  currentSong$!: Observable<SongData | null>;

  constructor(private contentCreationService: ContentCreationService) {}

  ngOnInit(): void {
    this.songs$ = this.contentCreationService.songs$;
    this.currentSong$ = this.contentCreationService.currentSong$;
  }
}
