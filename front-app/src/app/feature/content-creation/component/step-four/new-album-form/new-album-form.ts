import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NgxNotifierService } from 'ngx-notifier';
import { filter, Subscription } from 'rxjs';
import { ContentCreationService } from '../../../service/content-creation.service';
import { AlbumCreation } from '../../../model/albumCreation';
import { fileTypeValidator } from '../../step-one/file-upload-step/fileTypeValidator';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-new-album-form',
  standalone: false,
  templateUrl: './new-album-form.html',
  providers: [DatePipe],
  styleUrl: './new-album-form.scss',
})
export class NewAlbumForm implements OnInit, OnDestroy {
  private readonly allowedFileTypes = ['jpg', 'jpeg', 'png'];

  nameFailureSub: Subscription | undefined | null = null;
  yearFailureSub: Subscription | undefined | null = null;
  imageFailureSub: Subscription | undefined | null = null;
  successSub: Subscription | undefined | null = null;

  constructor(
    private notifier: NgxNotifierService,
    private creationService: ContentCreationService,
    private datePipe: DatePipe
  ) {}

  newAlbumForm: FormGroup = new FormGroup({
    image: new FormControl<FileList | null>(null, [
      Validators.required,
      fileTypeValidator([...this.allowedFileTypes]),
    ]),
    name: new FormControl('', [Validators.required]),
    year: new FormControl<Date | null>(null, [
      Validators.required,
      (control) => {
        const value = control.value;
        if (value && new Date(value) > new Date()) {
          return { futureDate: true }; // can’t be in the future
        }
        return null;
      },
    ]),
  });

  get imageControl() {
    return this.newAlbumForm.get('image');
  }
  get nameControl() {
    return this.newAlbumForm.get('name');
  }

  get yearControl() {
    return this.newAlbumForm.get('year');
  }

  ngOnInit(): void {
    this.nameFailureSub = this.nameControl?.statusChanges
      .pipe(filter((s) => s === 'INVALID'))
      .subscribe(() => {
        this.notifier.createToast('Name is required', 'danger', 3000);
      });

    this.yearFailureSub = this.yearControl?.statusChanges
      .pipe(filter((s) => s === 'INVALID'))
      .subscribe(() => {
        this.notifier.createToast('Year is required', 'danger', 3000);
      });
    this.imageFailureSub = this.imageControl?.statusChanges
      .pipe(filter((s) => s === 'INVALID'))
      .subscribe(() => {
        let message = '';
        const errors = this.imageControl?.errors;
        if (errors?.['required']) message = 'Image is required';
        else if (errors?.['fileType'])
          message =
            'File type must be one of these: ' +
            [...this.allowedFileTypes].join(', ');
        this.notifier.createToast(message, 'danger', 3000);
      });
    this.successSub = this.newAlbumForm.statusChanges
      .pipe(filter((s) => s === 'VALID'))
      .subscribe(() => {
        this.creationService.setCreatedAlbum({
          image: this.imageControl?.value[0],
          name: this.nameControl?.value,
          releaseDate: this.getFormattedDate(),
        } as AlbumCreation);
      });
  }
  getFormattedDate() {
    const date = this.yearControl?.value;
    return date ? this.datePipe.transform(date, 'dd-MM-yyyy')! : '';
  }
  onFileChange(event: any) {
    const files = event.target.files;
    if (files && files.length > 0) {
      this.imageControl?.setValue(files);
    }
  }
  ngOnDestroy(): void {
    this.nameFailureSub?.unsubscribe();
    this.yearFailureSub?.unsubscribe();
    this.successSub?.unsubscribe();
    this.imageFailureSub?.unsubscribe();
  }
}
