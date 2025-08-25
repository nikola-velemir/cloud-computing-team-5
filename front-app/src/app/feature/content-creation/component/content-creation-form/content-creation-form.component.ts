import { Component, OnInit } from '@angular/core';
import { ContentCreationService } from '../../service/content-creation.service';
import { catchError, EMPTY, from, mergeMap, of, switchMap } from 'rxjs';
import { ContentCreationApi } from '../../service/content-creation-api';
import { AlbumState } from '../step-four/album-form/album-form';
import { NgxNotifier, NgxNotifierService } from 'ngx-notifier';

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
    private api: ContentCreationApi,
    private notifier: NgxNotifierService
  ) {}

  ngOnInit(): void {
    this.currentStep$ = this.contentCreationService.currentStep$;

    this.currentStep$.subscribe((step) => (this.currentStep = step));
  }

  submit(state: AlbumState) {
    switch (state) {
      case AlbumState.ALBUM: {
        this.uploadWithExistingAlbum();
        break;
      }
      case AlbumState.NEW_ALBUM: {
        this.uploadWithNewAlbum();
        break;
      }
      case AlbumState.SINGLE: {
        this.api.createAsSingles();
        break;
      }
    }
  }
  private uploadWithExistingAlbum() {
    const songs = this.contentCreationService.getSongs();
    const album = this.contentCreationService.getCurrentAlbum();
    console.log(songs);
    from(songs)
      .pipe(
        mergeMap((song) => {
          const formData = new FormData();
          formData.append('songName', song.songName ?? '');
          formData.append(
            'artists',
            JSON.stringify(song.artists.map((a) => a.id))
          );
          formData.append('image', song.songImage!);
          formData.append('audio', song.songAudio!);
          formData.append('genreId', song.songGenre?.id ?? '');
          formData.append('albumId', album ?? '');
          return this.api.createWithAlbum(formData).pipe(
            catchError((err) => {
              this.notifier.createToast(`Failed to upload ${song.songName}`);
              return EMPTY;
            })
          );
        }, 5)
      )
      .subscribe({
        error: (err) => this.notifier.createToast('Upload failed', err),
        complete: () => this.notifier.createToast('All songs uploaded!'),
      });
  }
  private uploadWithNewAlbum() {
    const songs = this.contentCreationService.getSongs();
    const album = this.contentCreationService.getCreatedAlbum();
    console.log(album);
    const albumFormData = new FormData();

    if (!album) return;

    albumFormData.append('albumName', album.name);
    albumFormData.append('albumImage', album.image);
    albumFormData.append(
      'artistIds',
      JSON.stringify(
        Array.from(
          new Set(songs.flatMap((song) => song.artists.map((a) => a.id)))
        )
      )
    );
    albumFormData.append('releaseDate', album.releaseDate);

    this.api
      .createAlbum(albumFormData)
      .pipe(
        catchError((err) => {
          this.notifier.createToast(
            `Failed to create album ${album?.name}`,
            'danger'
          );
          return EMPTY;
        }),
        switchMap((album) =>
          from(songs).pipe(
            mergeMap((song) => {
              const formData = new FormData();
              formData.append('songName', song.songName ?? '');
              formData.append(
                'artists',
                JSON.stringify(song.artists.map((a) => a.id))
              );
              formData.append('image', song.songImage!);
              formData.append('audio', song.songAudio!);
              formData.append('genreId', song.songGenre?.id ?? '');
              formData.append('albumId', album.albumId);
              return this.api.createWithAlbum(formData).pipe(
                catchError((err) => {
                  this.notifier.createToast(
                    `Failed to upload ${song.songName}`
                  );
                  return EMPTY;
                })
              );
            }, 5)
          )
        )
      )
      .subscribe({
        next: (res) => console.log(res),
        error: (err) => this.notifier.createToast('Upload failed', err),
        complete: () => console.log('All songs uploaded!'),
      });
  }
}
