import { Component } from '@angular/core';
import {FormArray, FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {NgForOf, NgIf} from '@angular/common';
import {GenreService} from '../../service/genre-service';
import {ListGenres} from '../../model/list-genres';
import {GenreResponse} from '../../model/genre-response';
import {ArtistService} from '../../service/artist-service';
import {CreateArtistDTO} from '../../model/create-artist-DTO';

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

  selectedGenreNames: string[] = [];
  selectedGenreIds: string[] = [];


  genres:GenreResponse[] = []

  constructor(private fb: FormBuilder, private genresService: GenreService, private artistService:ArtistService) {}

  ngOnInit(): void {
    this.artistForm = this.fb.group({
      name: ['', Validators.required],
      biography: ['', Validators.required],
      genres: this.buildGenresArray()
    });
    this.getGenres();
  }

  getGenres(){
    this.genresService.getAllGenres().subscribe({
      next: (res) =>{
        this.genres = res.genres
      },
      error: (err) => {
        console.log(err);
      }
    })
  }

  toggleGenre(genre: GenreResponse, event: any) {
    if (event.target.checked) {
      this.selectedGenreNames.push(genre.name);
      this.selectedGenreIds.push(genre.id);
    } else {
      this.selectedGenreNames = this.selectedGenreNames.filter(name => name !== genre.name);
      this.selectedGenreIds = this.selectedGenreIds.filter(id => id !== genre.id);
    }
  }

  private buildGenresArray(): FormArray {
    const arr = this.genres.map(() => new FormControl(false));
    return this.fb.array(arr);
  }

  // custom validator TODO
  private minSelectedCheckboxes(min: number) {
    return (formArray: FormArray) => {
      const totalSelected = formArray.controls
        .map(control => control.value)
        .reduce((prev, next) => next ? prev + 1 : prev, 0);
      return totalSelected >= min ? null : { required: true };
    };
  }

  onSubmit(): void {
    if (this.artistForm.invalid) return;

    const selectedGenres = this.artistForm.value.genres
      .map((checked: boolean, i: number) => checked ? this.genres[i] : null)
      .filter((v: string | null) => v !== null);

    const payload : CreateArtistDTO= {
      name: this.artistForm.value.name,
      biography: this.artistForm.value.biography,
      genres_id: this.selectedGenreIds
    };

    this.artistService.createArtist(payload).subscribe({
      next: (res) => {
        console.log(res);
      },
      error: (err) => {
        console.log(err);
      }
    })

  }
}
