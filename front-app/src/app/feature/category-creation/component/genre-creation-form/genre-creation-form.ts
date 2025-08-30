import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NgxNotifierService } from 'ngx-notifier';
import { filter, Subscription, switchMap } from 'rxjs';
import { GenreService } from '../../service/genre-service';
import { fileTypeValidator } from '../../fileTypeValidator';
import { GenreCreationRequest } from '../../model/GenreCreationRequest';

@Component({
  selector: 'app-genre-creation-form',
  standalone: false,
  templateUrl: './genre-creation-form.html',
  styleUrl: './genre-creation-form.scss',
})
export class GenreCreationForm implements OnInit, OnDestroy {
  constructor(
    private notifier: NgxNotifierService,
    private service: GenreService
  ) {}

  readonly validImageFormats = ['ico'];

  imagePreview: string | ArrayBuffer | null = null;

  imageFailureSub: Subscription | null | undefined = null;
  imageSuccessSub: Subscription | null | undefined = null;
  nameFailureSub: Subscription | null | undefined = null;
  genreFormGroup: FormGroup = new FormGroup({
    genreImage: new FormControl<FileList | null>(null, [
      Validators.required,
      fileTypeValidator([...this.validImageFormats]),
    ]),
    description: new FormControl<string>('', Validators.required),
    name: new FormControl<string>('', Validators.required),
  });

  get image() {
    return this.genreFormGroup.get('genreImage');
  }
  get name() {
    return this.genreFormGroup.get('name');
  }
  get description() {
    return this.genreFormGroup.get('description');
  }

  ngOnInit(): void {
    this.imageFailureSub = this.image?.statusChanges
      .pipe(filter((s) => s === 'INVALID'))
      .subscribe(() => {
        const errors = this.image?.errors;
        let message = '';
        if (errors?.['required']) message = 'Image is required';
        else if (errors?.['fileType'])
          message =
            'Image must be of format ' + [...this.validImageFormats].join(', ');

        this.notifier.createToast(message, 'danger', 3000);
      });
    this.imageSuccessSub = this.image?.statusChanges
      .pipe(filter((s) => s === 'VALID'))
      .subscribe(() => {
        const file = this.image?.value;
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          this.imagePreview = reader.result;
        };
        reader.readAsDataURL(file[0]);
      });
    this.nameFailureSub = this.name?.statusChanges
      .pipe(filter((s) => s === 'INVALID'))
      .subscribe(() => {
        this.notifier.createToast('Genre name is required', 'danger', 3000);
      });
  }
  ngOnDestroy(): void {
    this.imageFailureSub?.unsubscribe();
    this.imageSuccessSub?.unsubscribe;
    this.imagePreview = null;
    this.nameFailureSub?.unsubscribe;
  }
  onFileChange(event: any) {
    const files = event.target.files;
    if (files && files.length > 0) {
      this.image?.setValue(files);
    }
  }
  onSubmit() {
    Object.values(this.genreFormGroup.controls).forEach((control) => {
      control.markAsTouched();
      control.updateValueAndValidity({ onlySelf: true, emitEvent: true });
    });

    if (this.genreFormGroup.invalid) return;

    const request: GenreCreationRequest = {
      description: this.description?.value,
      name: this.description?.value,
    };
    const file = this.image?.value;
    if (!file) return;
    this.service
      .createGenre(request)
      .pipe(
        switchMap((r) => {
          console.log(r);

          return this.service.requestGenreIconUpload({ genreId: r.genreId });
        })
      )
      .pipe(
        switchMap((r) => {
          const contentType = 'image/x-icon';
          return this.service.uploadGenreIcon(r.uploadUrl, file, contentType);
        })
      )
      .subscribe(() => {
        this.notifier.createToast(
          'Successfully created a category',
          'success',
          3000
        );
      });
  }
}
