import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DiscoverPage } from './component/discover-page/discover-page';
import { FormsModule } from '@angular/forms';
import { SongCard } from './component/song-card/song-card';
import { RouterLink } from '@angular/router';

@NgModule({
  declarations: [DiscoverPage, SongCard],
  imports: [CommonModule, FormsModule, RouterLink],
})
export class DiscoverPageModule {}
