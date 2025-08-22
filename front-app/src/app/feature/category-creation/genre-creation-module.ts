import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GenreCreationForm } from './genre-creation-form/genre-creation-form';
import { ReactiveFormsModule } from '@angular/forms';
import { GenreService } from './service/genre-service';

@NgModule({
  declarations: [GenreCreationForm],
  imports: [CommonModule, ReactiveFormsModule],
  exports: [GenreCreationForm],
  providers: [GenreService],
})
export class GenreCreationModule {}
