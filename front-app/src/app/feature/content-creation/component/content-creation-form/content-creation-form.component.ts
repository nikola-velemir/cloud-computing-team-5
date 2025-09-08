import { Component, OnInit } from '@angular/core';
import { ContentCreationService } from '../../service/content-creation.service';
import { catchError, EMPTY, from, mergeMap, of, switchMap, tap } from 'rxjs';
import {
  ContentCreationApi,
  CreateAlbumRequest,
  CreateSongAsSingleRequest,
  CreateSongWithAlbumRequest,
} from '../../service/content-creation-api';
import { AlbumState } from '../step-four/album-form/album-form';
import { NgxNotifierService } from 'ngx-notifier';
import { LoadingItemModel } from '../loading-item/loading-item';

@Component({
  selector: 'app-content-creation-form',
  standalone: false,
  templateUrl: './content-creation-form.component.html',
  styleUrl: './content-creation-form.component.scss',
})
export class ContentCreationForm implements OnInit {
  currentStep$ = of(0);
  currentStep = 0;

  isUploading = false;
  uploadingItems: LoadingItemModel[] = [];
  constructor(
    private contentCreationService: ContentCreationService,
    private api: ContentCreationApi,
    private notifier: NgxNotifierService
  ) {}

  ngOnInit(): void {
    this.currentStep$ = this.contentCreationService.currentStep$;

    this.currentStep$.subscribe((step) => (this.currentStep = step));
    this.contentCreationService.songs$.subscribe((v) => console.log(v));
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
        this.uploadAsSingles();
        break;
      }
    }
  }
  uploadAsSingles() {
    const songs = this.contentCreationService.getSongs();
    this.isUploading = true;
    this.uploadingItems = [];

    from(songs)
      .pipe(
        mergeMap((song) => {
          const index =
            this.uploadingItems.push({
              name: song.songName ?? 'Untitlted',
              status: 'inProgress',
              statusMessage: 'Uploading song...',
            }) - 1;

          const request: CreateSongAsSingleRequest = {
            duration: song.songDuration,
            artistIds: song.artists.map((a) => a.id),
            genreId: song.songGenre?.id ?? '',
            name: song.songName ?? '',
            audioType: song.songImage?.type ?? '',
            imageType: song.songAudio?.type ?? '',
          };
          if (!song.songAudio || !song.songImage) {
            this.uploadingItems[index] = {
              ...this.uploadingItems[index],
              status: 'failed',
              statusMessage: 'Missing files',
            };
            return EMPTY;
          }
          return this.api
            .createSongAsSingle(request, song.songAudio, song.songImage)
            .pipe(
              catchError(() => {
                this.uploadingItems[index] = {
                  ...this.uploadingItems[index],
                  status: 'failed',
                  statusMessage: 'Failed to upload',
                };

                return EMPTY;
              }),
              tap(() => {
                this.uploadingItems[index] = {
                  ...this.uploadingItems[index],
                  status: 'done',
                  statusMessage: 'Song uploaded',
                };
              })
            );
        }, 3)
      )
      .subscribe({
        error: (err) => this.notifier.createToast('Upload failed', err),
        complete: () => this.notifier.createToast('All songs uploaded!'),
      });
  }
  private uploadWithExistingAlbum() {
    const songs = this.contentCreationService.getSongs();
    const album = this.contentCreationService.getCurrentAlbum();

    this.isUploading = true;
    this.uploadingItems = [];
    from(songs)
      .pipe(
        mergeMap((song) => {
          const index =
            this.uploadingItems.push({
              name: song.songName ?? 'Untitlted',
              status: 'inProgress',
              statusMessage: 'Uploading song...',
            }) - 1;

          const request: CreateSongWithAlbumRequest = {
            duration: song.songDuration,
            artistIds: song.artists.map((a) => a.id),
            genreId: song.songGenre?.id ?? '',
            name: song.songName ?? '',
            albumId: album ?? '',
            audioType: song.songAudio?.type ?? '',
            imageType: song.songImage?.type ?? '',
          };
          if (!song.songAudio || !song.songImage) {
            this.uploadingItems[index] = {
              ...this.uploadingItems[index],
              status: 'failed',
              statusMessage: 'Missing files',
            };
            return EMPTY;
          }
          return this.api
            .createSongWithAlbum(request, song.songAudio, song.songImage)
            .pipe(
              catchError(() => {
                this.uploadingItems[index] = {
                  ...this.uploadingItems[index],
                  status: 'failed',
                  statusMessage: 'Failed to upload',
                };

                return EMPTY;
              }),
              tap(() => {
                this.uploadingItems[index] = {
                  ...this.uploadingItems[index],
                  status: 'done',
                  statusMessage: 'Song uploaded',
                };
              })
            );
        }, 3)
      )
      .subscribe({
        error: (err) => this.notifier.createToast('Upload failed', err),
        complete: () => this.notifier.createToast('All songs uploaded!'),
      });
  }
  private uploadWithNewAlbum() {
    const songs = this.contentCreationService.getSongs();
    const createdAlbum = this.contentCreationService.getCreatedAlbum();
    const albumCreateRequest: CreateAlbumRequest = {
      imageType: createdAlbum?.image.type ?? '',
      genreIds: Array.from(new Set(songs.map((s) => s.songGenre?.id))).filter(
        (s) => s !== undefined
      ),
      title: createdAlbum?.name ?? '',
      artistIds: Array.from(
        new Set(songs.flatMap((s) => s.artists.map((a) => a.id)))
      ),
      releaseDate: createdAlbum?.releaseDate ?? '',
    };
    console.log(albumCreateRequest);
    if (!createdAlbum?.image) return;
    this.isUploading = true;
    this.uploadingItems = [];
    this.uploadingItems.push({
      name: createdAlbum.name,
      statusMessage: 'Uploading album...',
      status: 'inProgress',
    });

    this.api
      .createAlbum(albumCreateRequest, createdAlbum.image)
      .pipe(
        catchError((v) => {
          this.uploadingItems[0] = {
            ...this.uploadingItems[0],
            status: 'failed',
            statusMessage: 'Failed to upload an album',
          };
          return EMPTY;
        }),
        switchMap((album) => {
          this.uploadingItems[0] = {
            ...this.uploadingItems[0],
            status: 'done',
            statusMessage: `Album uploaded`,
          };
          return from(songs).pipe(
            mergeMap((song) => {
              const index =
                this.uploadingItems.push({
                  name: song.songName ?? 'Untitlted',
                  status: 'inProgress',
                  statusMessage: 'Uploading song...',
                }) - 1;

              const request: CreateSongWithAlbumRequest = {
                duration: song.songDuration,
                artistIds: song.artists.map((a) => a.id),
                genreId: song.songGenre?.id ?? '',
                name: song.songName ?? '',
                albumId: album,
                audioType: song.songAudio?.type ?? '',
                imageType: song.songImage?.type ?? '',
              };
              if (!song.songAudio || !song.songImage) {
                this.uploadingItems[index] = {
                  ...this.uploadingItems[index],
                  status: 'failed',
                  statusMessage: 'Missing files',
                };
                return EMPTY;
              }
              return this.api
                .createSongWithAlbum(request, song.songAudio, song.songImage)
                .pipe(
                  catchError(() => {
                    this.uploadingItems[index] = {
                      ...this.uploadingItems[index],
                      status: 'failed',
                      statusMessage: 'Failed to upload',
                    };

                    return EMPTY;
                  }),
                  tap(() => {
                    this.uploadingItems[index] = {
                      ...this.uploadingItems[index],
                      status: 'done',
                      statusMessage: 'Song uploaded',
                    };
                  })
                );
            }, 3)
          );
        })
      )
      .subscribe({
        error: (err) => this.notifier.createToast('Upload failed', err),
        complete: () => this.notifier.createToast('All songs uploaded!'),
      });
  }
}
