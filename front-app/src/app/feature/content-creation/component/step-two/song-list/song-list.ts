import { Component, OnInit } from '@angular/core';
import {
  ContentCreationService,
  SongData,
} from '../../../service/content-creation.service';
import { AsyncPipe, NgForOf } from '@angular/common';
import { Observable } from 'rxjs';
import { SongListItem } from '../song-list-item/song-list-item';

@Component({
  selector: 'content-creation-song-list',
  imports: [NgForOf, AsyncPipe, SongListItem],
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
