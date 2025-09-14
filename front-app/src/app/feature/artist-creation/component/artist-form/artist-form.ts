import {Component, EventEmitter, Output} from '@angular/core';
import {
  AbstractControl,
  FormArray,
  FormBuilder,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidatorFn,
  Validators
} from '@angular/forms';
import {NgForOf, NgIf} from '@angular/common';
import {GenreService} from '../../service/genre-service';
import {ListGenres} from '../../model/list-genres';
import {GenreResponse} from '../../model/genre-response';
import {ArtistService} from '../../service/artist-service';
import {CreateArtistDTO} from '../../model/create-artist-DTO';
import {ToastService} from '../../../../shared/toast/service/toast-service';

@Component({
  selector: 'app-artist-form',
  imports: [
    ReactiveFormsModule,
    NgForOf,
    NgIf
  ],
  templateUrl: './artist-form.html',
  styleUrl: './artist-form.scss'
})
export class ArtistForm {
  artistForm!: FormGroup;
  waitingResponse = false;

  selectedGenreNames: string[] = [];
  selectedGenreIds: string[] = [];
  @Output() artistCreated = new EventEmitter<void>();

  genres:GenreResponse[] = []

  constructor(private fb: FormBuilder, private genresService: GenreService,
              private artistService:ArtistService, private toast:ToastService) {}

  ngOnInit(): void {
    this.artistForm = this.fb.group({
      name: ['', Validators.required],
      biography: ['', Validators.required],
      genres: this.fb.array([], this.minSelectedCheckboxes(1))
    });
    this.getGenres();
  }

  getGenres(){
    this.genresService.getAllGenres().subscribe({
      next: (res) => {
        this.genres = res.genres;

        const genresArray = this.genresFormArray;
        this.genres.forEach(() => genresArray.push(new FormControl(false)));
      },
      error: (err) => {
        this.toast.error(err.errorr || "Error");
      }
    });
  }

  get genresFormArray(): FormArray {
    return this.artistForm.get('genres') as FormArray;
  }

  private minSelectedCheckboxes(min: number): ValidatorFn {
    return (formArray: AbstractControl) => {
      const array = formArray as FormArray;
      const totalSelected = array.controls
        .map(c => c.value)
        .reduce((sum, val) => val ? sum + 1 : sum, 0);

      return totalSelected >= min ? null : { required: true };
    };
  }


  onSubmit(): void {
    if (this.artistForm.invalid) return;

    const selectedGenreIds = this.genresFormArray.controls
      .map((c, i) => c.value ? this.genres[i].id : null)
      .filter(id => id !== null) as string[];

    const payload: CreateArtistDTO = {
      name: this.artistForm.value.name,
      biography: this.artistForm.value.biography,
      genres_id: selectedGenreIds
    };

    this.waitingResponse = true;

    this.artistService.createArtist(payload).subscribe({
      next: () => {
        this.toast.success("Artist created successfully");
        this.artistCreated.emit();
        this.artistForm.reset();
        this.genresFormArray.controls.forEach(c => c.setValue(false));
      },
      error: (err) => {
        this.toast.error(err.errorr || "Error");
      },
      complete: () => {
        this.waitingResponse = false;
      }
    });
  }
}
