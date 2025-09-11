import { Component } from '@angular/core';
import {FormArray, FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {NgForOf, NgIf} from '@angular/common';

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

  genres: string[] = ['Rock', 'Pop', 'Jazz', 'Hip-Hop', 'Classical'];

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.artistForm = this.fb.group({
      name: ['', Validators.required],
      biography: ['', Validators.required],
      genres: this.buildGenresArray()
    });
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

    const payload = {
      name: this.artistForm.value.name,
      biography: this.artistForm.value.biography,
      genres: selectedGenres
    };

    console.log('Artist payload:', payload);

  }
}
