import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { GenreService } from './service/genre-service';
import { GenreCreationForm } from './component/genre-creation-form/genre-creation-form';

@NgModule({
  declarations: [GenreCreationForm],
  imports: [CommonModule, ReactiveFormsModule],
  exports: [],
  providers: [GenreService],
})
export class GenreCreationModule {}
