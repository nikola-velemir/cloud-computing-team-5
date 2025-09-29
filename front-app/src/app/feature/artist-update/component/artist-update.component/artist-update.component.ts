import { Component, Input, OnInit } from '@angular/core';
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
import { Artist } from '../../model/artist.mode';

@Component({
  selector: 'app-artist-update',
  standalone: false,
  templateUrl: './artist-update.component.html',
  styleUrl: './artist-update.component.scss',
})
export class ArtistUpdateComponent implements OnInit {
  artistForm: any;
  @Input() artistId!: string;
  genres: any;
  waitingResponse: any;

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
    this.getGenres();
    this.artistService.getArtist(this.artistId).subscribe({
      next: (response: Artist) => {
        console.log(response);
        this.artistForm.patchValue({
          name: response.name,
          biography: response.biography,
        });
      },
    });
  }
  onSubmit() {
    throw new Error('Method not implemented.');
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

  getGenres() {
    this.genresService.getAllGenres().subscribe({
      next: (res) => {
        this.genres = res.genres;

        const genresArray = this.genresFormArray;
        this.genres.forEach(() => genresArray.push(new FormControl(false)));
      },
      error: (err) => {
        this.toast.error(err.errorr || 'Error');
      },
    });
  }
}
