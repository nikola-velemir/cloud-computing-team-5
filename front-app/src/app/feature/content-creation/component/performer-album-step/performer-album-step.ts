import {
  Component,
  EventEmitter,
  OnDestroy,
  OnInit,
  Output,
} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Author} from '../../model/author';
import {Album} from '../../model/album';
import {ContentCreationService} from '../../service/content-creation.service';
import {filter, Subscription, switchMap, take} from 'rxjs';
import {NgxNotifierService} from 'ngx-notifier';
import createPlugin from 'tailwindcss/plugin';
import withOptions = createPlugin.withOptions;

export enum AlbumState {
  ALBUM,
  SINGLE,
  NEW_ALBUM,
}

@Component({
  selector: 'content-creation-performer-album-step',
  standalone: false,
  templateUrl: './performer-album-step.html',
  styleUrl: './performer-album-step.scss',
})
export class PerformerAlbumStep implements OnInit, OnDestroy {
  AlbumState = AlbumState;

  constructor(
    private contentCreationService: ContentCreationService,
    private notifier: NgxNotifierService
  ) {
  }

  @Output() onSubmit = new EventEmitter<AlbumState>();

  performerFailureSub: Subscription | null | undefined = null;

  readonly mockAlbums: Album[] = [
    {
      id: 1,
      name: 'Midnight Echoes',
      year: '2019',
      author: 'Luna Waves',
      trackNum: 12,
    },
    {
      id: 2,
      name: 'Electric Horizon',
      year: '2020',
      author: 'Neon Skies',
      trackNum: 10,
    },
    {
      id: 3,
      name: 'Golden Dusk',
      year: '2018',
      author: 'Aurora Vale',
      trackNum: 14,
    },
    {
      id: 4,
      name: 'Silent Streets',
      year: '2021',
      author: 'Urban Drift',
      trackNum: 9,
    },
    {
      id: 5,
      name: 'Ocean Dreams',
      year: '2017',
      author: 'Blue Tide',
      trackNum: 11,
    },
    {
      id: 6,
      name: 'Velvet Shadows',
      year: '2022',
      author: 'Crimson Noir',
      trackNum: 13,
    },
    {
      id: 7,
      name: 'Silver Rain',
      year: '2016',
      author: 'Misty Vale',
      trackNum: 8,
    },
    {
      id: 8,
      name: 'Skyward Bound',
      year: '2023',
      author: 'Cloudchaser',
      trackNum: 15,
    },
    {
      id: 9,
      name: 'Amber Lights',
      year: '2020',
      author: 'Golden Beats',
      trackNum: 10,
    },
    {
      id: 10,
      name: 'Frostfire',
      year: '2021',
      author: 'Arctic Flame',
      trackNum: 12,
    },
  ];
  readonly mockAuthors: Author[] = [
    {id: 1, name: 'Luna Waves'},
    {id: 2, name: 'Neon Skies'},
    {id: 3, name: 'Aurora Vale'},
  ];

  performerAlbumForm = new FormGroup({
    performers: new FormControl<Author[]>([], [Validators.required]),
    creationType: new FormControl(AlbumState.ALBUM, [Validators.required]),
    album: new FormControl<Album | null>(null),
  });

  ngOnInit(): void {
    this.performerFailureSub = this.performers?.statusChanges
      .pipe(filter((s) => s === 'INVALID'))
      .subscribe(() => {
        this.notifier.createToast(
          'You must select at least one performer',
          'danger',
          3000
        );
      });
    this.creationType?.setValue(AlbumState.ALBUM);
    this.creationType?.valueChanges
      .pipe(filter((v) => v !== AlbumState.NEW_ALBUM))
      .subscribe((c) => {
        this.contentCreationService.clearAlbumCreation();
        this.album?.setValue(null)
      });

    this.creationType?.valueChanges
      .pipe(filter((v) => v === AlbumState.ALBUM))
      .subscribe((c) => {
        if (this.album?.value == null)
          this.notifier.createToast('You must select an album', 'danger', 3000);
      });
  }

  ngOnDestroy(): void {
    this.performerFailureSub?.unsubscribe();
  }

  get performers() {
    return this.performerAlbumForm.get('performers');
  }

  get creationType() {
    return this.performerAlbumForm.get('creationType');
  }

  get album() {
    return this.performerAlbumForm.get('album');
  }

  onPerformerToggle(event: Author): void {
    const exists =
      this.performers?.value?.some((a: Author) => a.id === event.id) ?? false;
    if (!exists)
      this.performers?.setValue([...(this.performers?.value ?? []), event]);
    else
      this.performers?.setValue(
        this.performers?.value?.filter((p) => p.id !== event.id) ?? []
      );
  }

  finish() {
    this.performers?.setValue(this.performers?.value ?? [], {
      emitEvent: true,
    });
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
    this.album?.setValue($event)
  }
}
