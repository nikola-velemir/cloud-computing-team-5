import {
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  ViewChild,
} from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { fileTypeValidator } from './fileTypeValidator';
import { filter, Subscription, take } from 'rxjs';
import { NgxNotifierService } from 'ngx-notifier';
import { ContentCreationService } from '../../../service/content-creation.service';
import { ContentCreationApi } from '../../../service/content-creation-api';

@Component({
  selector: 'content-creation-file-upload-step',
  templateUrl: './file-upload-step.html',
  standalone: false,
  styleUrls: ['./file-upload-step.scss'],
})
export class FileUploadStep implements OnInit, OnDestroy {
  @ViewChild('audioEl') audioEl!: ElementRef<HTMLAudioElement>;
  constructor(
    private contentCreationService: ContentCreationService,
    private notifier: NgxNotifierService,
    private api: ContentCreationApi
  ) {}

  fileGroup: FormGroup = new FormGroup({
    musicFile: new FormControl<FileList | null>(null, [
      Validators.required,
      fileTypeValidator(['mp3']),
    ]),
  });
  successSub: Subscription | null = null;
  failureSub: Subscription | null = null;

  onFileChange(event: any) {
    const files = event.target.files;
    if (files && files.length > 0) {
      //  this.loadAudioMetadata(files[0]); // load metadata for the first file
      this.fileGroup.get('musicFile')?.setValue(files);
      this.fileGroup.get('musicFile')?.updateValueAndValidity();
    }
  }

  ngOnInit(): void {
    const fileControl = this.fileGroup.get('musicFile');
    if (!fileControl) return;
    this.successSub = fileControl.statusChanges
      .pipe(
        filter((status) => status === 'VALID'),
        take(1)
      )
      .subscribe(() => {
        this.contentCreationService.initializeSongs(fileControl.value.length);
        this.contentCreationService.setSongAudios(fileControl.value);
        this.contentCreationService.setCurrentSong(0);
        this.contentCreationService.setCurrentStep(1);
      });
    this.failureSub = fileControl.statusChanges
      .pipe(
        filter((status) => status === 'INVALID'),
        take(1)
      )
      .subscribe(() => {
        const errors = fileControl.errors;
        let message = 'Invalid file';

        if (errors?.['required']) {
          message = 'File is required';
        } else if (errors?.['fileType']) {
          message = 'Wrong file type! Only MP3 allowed';
        }

        this.notifier.createToast(message, 'danger', 5000);
      });
  }

  ngOnDestroy() {
    this.successSub?.unsubscribe();
    this.failureSub?.unsubscribe();
  }
  private loadAudioMetadata(file: File) {
    const url = URL.createObjectURL(file);
    this.audioEl.nativeElement.src = url;
  }

  onMetadataLoaded(): void {
    const el = this.audioEl.nativeElement;
    const dur = el.duration;
    console.log(dur);
    URL.revokeObjectURL(el.src);
  }
}
