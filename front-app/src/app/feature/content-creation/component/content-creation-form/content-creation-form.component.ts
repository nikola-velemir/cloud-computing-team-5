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
        const songs = this.contentCreationService.getSongs();
        console.log(songs);
        const formData = new FormData();
        formData.append('songName', songs[0].songName ?? '');
        formData.append(
          'artists',
          JSON.stringify(songs[0].artists.map((a) => a.id))
        );
        formData.append('image', songs[0].songImage!);
        formData.append('audio', songs[0].songAudio!);
        formData.append('genreId', songs[0].songGenre?.id ?? '');
        this.api.createWithAlbum(formData).subscribe((c) => console.log(c));
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
