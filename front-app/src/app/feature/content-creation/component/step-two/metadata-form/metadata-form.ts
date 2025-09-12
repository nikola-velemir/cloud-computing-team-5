import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Genre } from '../../../model/genre';
import { NgxNotifierService } from 'ngx-notifier';
import { filter, Observable, Subscription } from 'rxjs';
import { ContentCreationService } from '../../../service/content-creation.service';
import { read } from 'fs';
import { fileTypeValidator } from '../../step-one/file-upload-step/fileTypeValidator';
import { GenreService } from '../../../service/genre-service';

@Component({
  selector: 'content-creation-metadata-form',
  standalone: false,
  templateUrl: './metadata-form.html',
  styleUrl: './metadata-form.scss',
})
export class MetadataForm implements OnInit, OnDestroy {
  imagePreview: string | ArrayBuffer | null = null;
  genres$: Observable<Genre[]>;

  constructor(
    private contentCreationService: ContentCreationService,
    private notifier: NgxNotifierService,
    private genreService: GenreService
  ) {
    this.genres$ = genreService.genres$;
  }

  metadataForm: FormGroup = new FormGroup({
    songImage: new FormControl<FileList | null>(null, [
      Validators.required,
      fileTypeValidator(['png', 'jpg', 'jpeg']),
    ]),
    songName: new FormControl('', [Validators.required]),
    selectedGenre: new FormControl<Genre | null>(null, [Validators.required]),
  });

  private successSub: Subscription | null = null;
  private songImageFailureSub: Subscription | null = null;
  private currentSongSub: Subscription | null = null;
  private genreFailureSub: Subscription | null = null;
  private songNameFailureSub: Subscription | null = null;

  onGenreSelect($event: Genre) {
    this.selectedGenre?.setValue($event);
    this.selectedGenre?.updateValueAndValidity();
  }

  onFileChange(event: any) {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;

    const files = event.target.files;
    if (files) {
      this.songImage?.setValue(files);
      this.songImage?.updateValueAndValidity();
    }
    const reader = new FileReader();
    reader.onload = () => {
      this.imagePreview = reader.result;
    };
    reader.readAsDataURL(files[0]);
  }

  get songImage() {
    return this.metadataForm.get('songImage');
  }

  get songName() {
    return this.metadataForm.get('songName');
  }

  get selectedGenre() {
    return this.metadataForm.get('selectedGenre');
  }

  ngOnInit(): void {
    const songImageControl = this.songImage;
    const nameControl = this.songName;
    const genreControl = this.selectedGenre;
    if (songImageControl)
      this.songImageFailureSub = songImageControl.statusChanges
        .pipe(filter((status) => status === 'INVALID'))
        .subscribe(() => {
          const errors = songImageControl.errors;
          let message = 'Invalid file';

          if (errors?.['required']) {
            message = 'Image is required';
          } else if (errors?.['fileType']) {
            message = 'Wrong file type! Only PNG, JPG, JPEG allowed';
          }

          this.notifier.createToast(message, 'danger', 5000);
        });
    if (nameControl)
      this.songNameFailureSub = nameControl.statusChanges
        .pipe(filter((status) => status === 'INVALID'))
        .subscribe(() => {
          const errors = nameControl.errors;
          let message = 'Invalid file';

          if (errors?.['required']) {
            message = 'Name is required';
          }
          this.notifier.createToast(message, 'danger', 5000);
        });
    if (genreControl)
      this.genreFailureSub = genreControl.statusChanges
        .pipe(filter((status) => status === 'INVALID'))
        .subscribe(() => {
          const errors = genreControl.errors;
          let message = 'Genre is required';

          if (errors?.['required']) {
            message = 'Genre is required';
          }
          this.notifier.createToast(message, 'danger', 5000);
        });
  }

  ngOnDestroy(): void {
    this.songImageFailureSub?.unsubscribe();
    this.successSub?.unsubscribe();
    this.genreFailureSub?.unsubscribe();
    this.songNameFailureSub?.unsubscribe();
    this.currentSongSub?.unsubscribe();
  }

  nextStep() {
    Object.values(this.metadataForm.controls).forEach((control) => {
      control.markAsTouched();
      control.updateValueAndValidity({ onlySelf: true, emitEvent: true });
    });
    if (this.metadataForm.invalid) return;
    const currentSong = this.contentCreationService.getCurrentSong();
    if (!currentSong) return;
    this.contentCreationService.setSongData(
      currentSong,
      this.songImage?.value[0],
      this.songName?.value,
      this.selectedGenre?.value
    );
    const result = this.contentCreationService.setNextSong(currentSong);
    if (!result) {
      this.contentCreationService.setCurrentStep(2);
      return;
    }
    this.songImage?.setValue(null);
    this.songName?.setValue('');
    this.imagePreview = null;
  }
}
