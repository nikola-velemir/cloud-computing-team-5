import { Component, OnInit } from '@angular/core';
import { ContentCreationService } from '../../service/content-creation.service';
import { of } from 'rxjs';
import { ContentCreationApi } from '../../service/content-creation-api';
import { AlbumState } from '../step-four/album-form/album-form';

@Component({
  selector: 'app-content-creation-form',
  standalone: false,
  templateUrl: './content-creation-form.component.html',
  styleUrl: './content-creation-form.component.scss',
})
export class ContentCreationForm implements OnInit {
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
