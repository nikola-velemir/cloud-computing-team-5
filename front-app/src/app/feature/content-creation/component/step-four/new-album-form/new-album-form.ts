import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NgxNotifierService } from 'ngx-notifier';
import { filter, Subscription } from 'rxjs';
import { ContentCreationService } from '../../../service/content-creation.service';
import { AlbumCreation } from '../../../model/albumCreation';

@Component({
  selector: 'app-new-album-form',
  standalone: false,
  templateUrl: './new-album-form.html',
  styleUrl: './new-album-form.scss',
})
export class NewAlbumForm implements OnInit, OnDestroy {
  nameFailureSub: Subscription | undefined | null = null;
  yearFailureSub: Subscription | undefined | null = null;
  successSub: Subscription | undefined | null = null;

  constructor(
    private notifier: NgxNotifierService,
    private creationService: ContentCreationService
  ) {}

  newAlbumForm: FormGroup = new FormGroup({
    name: new FormControl('', [Validators.required]),
    year: new FormControl('', [
      Validators.required,
      Validators.max(new Date().getFullYear()),
    ]),
  });

  ngOnInit(): void {
    const nameControl = this.newAlbumForm.get('name');
    const yearControl = this.newAlbumForm.get('year');
    if (nameControl)
      this.nameFailureSub = nameControl.statusChanges
        .pipe(filter((s) => s === 'INVALID'))
        .subscribe(() => {
          this.notifier.createToast('Name is required', 'danger', 3000);
        });

    if (yearControl)
      this.yearFailureSub = yearControl.statusChanges
        .pipe(filter((s) => s === 'INVALID'))
        .subscribe(() => {
          this.notifier.createToast('Year is required', 'danger', 3000);
        });
    if (yearControl && nameControl)
      this.successSub = this.newAlbumForm.statusChanges
        .pipe(filter((s) => s === 'VALID'))
        .subscribe(() =>
          this.creationService.setCreatedAlbum({
            name: nameControl.value,
            year: nameControl.value,
          } as AlbumCreation)
        );
  }

  ngOnDestroy(): void {
    this.nameFailureSub?.unsubscribe();
    this.yearFailureSub?.unsubscribe();
  }
}
