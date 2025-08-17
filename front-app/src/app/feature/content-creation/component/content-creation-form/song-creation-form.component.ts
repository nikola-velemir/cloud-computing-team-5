import { Component, OnInit } from '@angular/core';
import { ContentCreationService } from '../../service/content-creation.service';
import { of } from 'rxjs';
import { AlbumState } from '../performer-album-step/performer-album-step';
import { ContentCreationApi } from '../../service/content-creation-api';

@Component({
  selector: 'app-content-creation-form',
  standalone: false,
  templateUrl: './song-creation-form.component.html',
  styleUrl: './song-creation-form.component.scss',
})
export class SongCreationForm implements OnInit {
  currentStep$ = of(0);
  currentStep = 0;

  constructor(
    private contentCreationService: ContentCreationService,
    private api: ContentCreationApi
  ) {}

  ngOnInit(): void {
    this.currentStep$ = this.contentCreationService.currentStep$;

    this.currentStep$.subscribe((step) => (this.currentStep = step));
  }

  submit(state: AlbumState) {
    switch (state) {
      case AlbumState.ALBUM: {
        this.api.createWithAlbum();
        break;
      }
      case AlbumState.NEW_ALBUM: {
        this.api.createOnNewAlbum();
        break;
      }
      case AlbumState.SINGLE: {
        this.api.createAsSingles();
        break;
      }
    }
  }
}
