import {Component, EventEmitter, OnChanges, OnDestroy, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {fileTypeValidator} from './fileTypeValidator';
import {filter, Subscription, take} from 'rxjs';
import {NgxNotifierService} from 'ngx-notifier';
import {ContentCreationService} from '../../service/content-creation.service';

@Component({
  selector: 'content-creation-file-upload-step',
  templateUrl: './file-upload-step.html',
  standalone: false,
  styleUrls: ['./file-upload-step.scss']
})
export class FileUploadStep implements OnInit, OnDestroy {
  constructor(private contentCreationService: ContentCreationService, private notifier: NgxNotifierService) {
  }

  fileGroup: FormGroup = new FormGroup({
    musicFile: new FormControl<File | null>(null, [Validators.required, fileTypeValidator(['mp3'])])
  });
  successSub: Subscription | null = null;
  failureSub: Subscription | null = null;

  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.fileGroup.get('musicFile')?.setValue(file);
      this.fileGroup.get('musicFile')?.updateValueAndValidity();
    }

  }

  ngOnInit(): void {
    const fileControl = this.fileGroup.get('musicFile');
    if (!fileControl) return;
    this.successSub = fileControl.statusChanges.pipe(filter(status => status === 'VALID'),take(1)).subscribe(() => {
      this.contentCreationService.setSongFile(fileControl.value);
      this.contentCreationService.nextStep();
    });
    this.failureSub = fileControl.statusChanges
      .pipe(filter(status => status === 'INVALID'), take(1))
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

}
