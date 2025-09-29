import { Component, EventEmitter, Output } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { NgxNotifierService } from 'ngx-notifier';
import { Subscription, Observable, of, filter } from 'rxjs';
import { Album } from '../../../model/album';
import { Artist } from '../../../model/artist';
import { AlbumService } from '../../../service/album-service';
import { ContentCreationService } from '../../../service/content-creation.service';
import { ArtistService } from '../../../service/performer-service';

export enum AlbumState {
  ALBUM,
  SINGLE,
  NEW_ALBUM,
}

@Component({
  selector: 'content-creation-album-form',
  standalone: false,
  templateUrl: './album-form.html',
  styleUrl: './album-form.scss',
})
export class AlbumForm {
  AlbumState = AlbumState;

  constructor(
    private contentCreationService: ContentCreationService,
    private notifier: NgxNotifierService,
    private albumService: AlbumService
  ) {}

  @Output() onSubmit = new EventEmitter<AlbumState>();

  albums$: Observable<Album[]> = of([]);
  albumForm = new FormGroup({
    creationType: new FormControl(AlbumState.ALBUM, [Validators.required]),
    album: new FormControl<Album | null>(null),
  });

  ngOnInit(): void {
    const artistIds = this.contentCreationService.getArtists().map((a) => a.id);
    console.log(artistIds);
    this.albums$ = this.albumService.getAlbums(artistIds);
    this.creationType?.setValue(AlbumState.ALBUM);
    this.creationType?.valueChanges
      .pipe(filter((v) => v !== AlbumState.NEW_ALBUM))
      .subscribe(() => {
        this.contentCreationService.clearAlbumCreation();
        this.album?.setValue(null);
      });
    this.album?.valueChanges.subscribe((v) => {
      if (v) this.contentCreationService.setExistingAlbum(v.id);
    });
    this.creationType?.valueChanges
      .pipe(filter((v) => v === AlbumState.ALBUM))
      .subscribe(() => {
        if (this.album?.value == null)
          this.notifier.createToast('You must select an album', 'danger', 3000);
      });
  }

  ngOnDestroy(): void {}

  get creationType() {
    return this.albumForm.get('creationType');
  }

  get album() {
    return this.albumForm.get('album');
  }

  finish() {
    switch (this.creationType?.value) {
      case AlbumState.ALBUM: {
        if (this.album?.value == null)
          this.notifier.createToast('You must select an album', 'danger', 3000);
        this.onSubmit.emit(AlbumState.ALBUM);
        break;
      }
      case AlbumState.NEW_ALBUM: {
        const createdAlbum = this.contentCreationService.getCreatedAlbum();
        if (createdAlbum === null)
          this.notifier.createToast('You must create an album', 'danger', 3000);
        this.onSubmit.emit(AlbumState.NEW_ALBUM);
        break;
      }
      case AlbumState.SINGLE: {
        this.onSubmit.emit(AlbumState.SINGLE);
        break;
      }
    }
  }
  onAlbumSelect($event: Album) {
    this.album?.setValue($event);
  }
}
