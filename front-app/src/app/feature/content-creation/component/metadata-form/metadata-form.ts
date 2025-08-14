import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Genre} from '../../model/genre';
import {fileTypeValidator} from '../file-upload-step/fileTypeValidator';
import {NgxNotifierService} from 'ngx-notifier';
import {filter, Subscription} from 'rxjs';
import {ContentCreationService} from '../../service/content-creation.service';

@Component({
  selector: 'content-creation-metadata-form',
  standalone: false,
  templateUrl: './metadata-form.html',
  styleUrl: './metadata-form.scss'
})
export class MetadataForm implements OnInit, OnDestroy {


  constructor(private contentCreationService: ContentCreationService, private notifier: NgxNotifierService) {
  }

  genres: Genre[] = [
    {id: 1, name: 'Rock'},
    {id: 2, name: 'Jazz'},
    {id: 3, name: 'Pop'},
    {id: 4, name: 'Hip-Hop'}
  ];

  metadataForm: FormGroup = new FormGroup({
    songImage: new FormControl<File | null>(null, [Validators.required, fileTypeValidator(['png', 'jpg', 'jpeg'])]),
    songName: new FormControl('', [Validators.required]),
    selectedGenre: new FormControl<Genre | null>(null, [Validators.required]),
  })

  private successSub: Subscription | null = null;
  private songImageFailureSub: Subscription | null = null;

  private genreFailureSub: Subscription | null = null;
  private songNameFailureSub: Subscription | null = null;

  onGenreSelect($event: Genre) {
    this.metadataForm.get('selectedGenre')?.setValue($event);
    this.metadataForm.get('selectedGenre')?.updateValueAndValidity();
  }

  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file)
      console.log(file);
    if (file) {
      console.log(file);
      this.metadataForm.get('songImage')?.setValue(file);
      this.metadataForm.get('songImage')?.updateValueAndValidity();
    }

  }

  ngOnInit(): void {
    const songImageControl = this.metadataForm.get("songImage")
    const nameControl = this.metadataForm.get("songName")
    const genreControl = this.metadataForm.get("selectedGenre")
    if (songImageControl)
      this.songImageFailureSub = songImageControl.statusChanges.pipe(filter(status => status === 'INVALID')).subscribe(() => {
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
      this.songNameFailureSub = nameControl.statusChanges.pipe(filter(status => status === 'INVALID')).subscribe(() => {

        const errors = nameControl.errors;
        let message = 'Invalid file';

        if (errors?.['required']) {
          message = 'Name is required';
        }
        this.notifier.createToast(message, 'danger', 5000);

      });
    if (genreControl)
      this.genreFailureSub = genreControl.statusChanges.pipe(filter(status => status === 'INVALID')).subscribe(() => {
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
  }

  nextStep() {
    Object.values(this.metadataForm.controls).forEach(control => {
      control.markAsTouched();
      control.updateValueAndValidity({onlySelf: true, emitEvent: true});
    });
    if (this.metadataForm.invalid)
      return;
    this.contentCreationService.setGenre(this.metadataForm.get('selectedGenre')?.value);
    this.contentCreationService.setSongImage(this.metadataForm.get('songImage')?.value);
    this.contentCreationService.setSongName(this.metadataForm.get('songName')?.value);
    this.contentCreationService.nextStep();
  }

}
