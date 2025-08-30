import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { NgxNotifierService } from 'ngx-notifier';
import { Subscription, Observable, of, filter } from 'rxjs';
import { Artist } from '../../../model/artist';
import { ContentCreationService } from '../../../service/content-creation.service';
import { ArtistService as ArtistService } from '../../../service/performer-service';

@Component({
  selector: 'content-creation-artist-step',
  standalone: false,
  templateUrl: './performer-album-step.html',
  styleUrl: './performer-album-step.scss',
})
export class ArtistStep implements OnInit, OnDestroy {
  constructor(
    private contentCreationService: ContentCreationService,
    private notifier: NgxNotifierService,
    private artistService: ArtistService
  ) {}

  performerFailureSub: Subscription | null | undefined = null;

  performers$: Observable<Artist[]> = of([]);
  peformerForm = new FormGroup({
    performers: new FormControl<Artist[]>([], [Validators.required]),
  });

  ngOnInit(): void {
    this.performers$ = this.artistService.performers$;
    this.performerFailureSub = this.performers?.statusChanges
      .pipe(filter((s) => s === 'INVALID'))
      .subscribe(() => {
        this.notifier.createToast(
          'You must select at least one performer',
          'danger',
          3000
        );
      });
  }

  ngOnDestroy(): void {
    this.performerFailureSub?.unsubscribe();
  }

  get performers() {
    return this.peformerForm.get('performers');
  }
  onPerformerToggle(event: Artist): void {
    const exists =
      this.performers?.value?.some((a: Artist) => a.id === event.id) ?? false;
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
    if (this.peformerForm.invalid) return;
    this.contentCreationService.setArtists(this.performers?.value ?? []);
    this.contentCreationService.setCurrentStep(3);
  }
}
