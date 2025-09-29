import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArtistUpdateComponent } from './component/artist-update.component/artist-update.component';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [ArtistUpdateComponent],
  imports: [CommonModule, ReactiveFormsModule],
  exports: [ArtistUpdateComponent],
})
export class ArtistUpdateModule {}
