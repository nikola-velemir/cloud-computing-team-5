import { Component, Input, OnInit } from '@angular/core';
import { AsyncPipe, NgClass, NgForOf } from '@angular/common';
import {
  ContentCreationService,
  SongData,
} from '../../../service/content-creation.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-song-list-item',
  standalone: false,
  templateUrl: './song-list-item.html',
  styleUrl: './song-list-item.scss',
})
export class SongListItem implements OnInit {
  @Input() song!: SongData;
  currentSong$!: Observable<SongData | null>;
  constructor(private contentCreationService: ContentCreationService) {}
  ngOnInit(): void {
    this.currentSong$ = this.contentCreationService.currentSong$;
  }
}
