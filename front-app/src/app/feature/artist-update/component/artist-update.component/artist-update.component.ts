import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import {
  AbstractControl,
  FormArray,
  FormBuilder,
  FormControl,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { ToastService } from '../../../../shared/toast/service/toast-service';
import { GenreService } from '../../../artist-creation/service/genre-service';
import { ArtistUpdateService } from '../../service/artist-update.service';
import { forkJoin } from 'rxjs';
import { Genre } from '../../model/genre.model';
import { UpdateArtistRequest } from '../../model/update-artist.request';

@Component({
  selector: 'app-artist-update',
  standalone: false,
  templateUrl: './artist-update.component.html',
  styleUrl: './artist-update.component.scss',
})
export class ArtistUpdateComponent implements OnInit {
  artistForm: any;
  @Input() artistId!: string;
  genres: Genre[] = [];
  waitingResponse: boolean = false;
  @Output() artistUpdated = new EventEmitter<void>();

  constructor(
    private fb: FormBuilder,
    private genresService: GenreService,
    private artistService: ArtistUpdateService,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.artistForm = this.fb.group({
      name: ['', Validators.required],
      biography: ['', Validators.required],
      genres: this.fb.array([], this.minSelectedCheckboxes(1)),
    });

    forkJoin({
      genres: this.genresService.getAllGenres(),
      artist: this.artistService.getArtist(this.artistId),
    }).subscribe({
      next: ({ genres, artist }) => {
        this.genres = genres.genres;
        const genresArray = this.genresFormArray;
        this.genres.forEach(() => genresArray.push(new FormControl(false)));

        this.artistForm.patchValue({
          name: artist.name,
          biography: artist.biography,
        });

        if (artist.genres) {
          this.setSelectedGenres(artist.genres);
        }
      },
      error: (err) => {
        this.toast.error(err.error || 'Error');
      },
    });
  }

  private setSelectedGenres(selectedGenres: any[]) {
    const genresArray = this.genresFormArray;

    this.genres.forEach((genre: any, index: number) => {
      const found = selectedGenres.some((sg) => sg.id === genre.id);
      if (found) {
        genresArray.at(index).setValue(true);
      }
    });
  }

  onSubmit() {
    if (this.artistForm.invalid) return;

    const selectedGenreIds = this.genresFormArray.controls
      .map((c, i) => (c.value ? this.genres[i].id : null))
      .filter((id) => id !== null) as string[];

    const payload: UpdateArtistRequest = {
      id: this.artistId,
      name: this.artistForm.value.name,
      biography: this.artistForm.value.biography,
      genres_id: selectedGenreIds,
    };

    this.waitingResponse = true;

    this.artistService.updateArtist(payload).subscribe({
      next: () => {
        this.toast.success('Artist updated successfully');
        this.artistUpdated.emit();
        this.artistForm.reset();
        this.genresFormArray.controls.forEach((c) => c.setValue(false));
      },
      error: (err) => {
        this.toast.error(err.errorr || 'Error');
      },
      complete: () => {
        this.waitingResponse = false;
      },
    });
  }

  get genresFormArray(): FormArray {
    return this.artistForm.get('genres') as FormArray;
  }

  private minSelectedCheckboxes(min: number): ValidatorFn {
    return (formArray: AbstractControl) => {
      const array = formArray as FormArray;
      const totalSelected = array.controls
        .map((c) => c.value)
        .reduce((sum, val) => (val ? sum + 1 : sum), 0);

      return totalSelected >= min ? null : { required: true };
    };
  }
}
