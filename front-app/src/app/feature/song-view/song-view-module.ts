import { NgModule } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { SongView } from './component/song-view/song-view';
import { AlbumCard } from './component/album-card/album-card';
import { PerformerCard } from './component/performer-card/performer-card';
import { RouterLink } from '@angular/router';
import { ReviewService } from './service/review.service';
import { SongPreviewService } from './service/song-preview';

@NgModule({
  declarations: [SongView, AlbumCard, PerformerCard],
  imports: [CommonModule, RouterLink, NgFor],
  providers: [ReviewService, SongPreviewService],
  exports: [SongView],
})
export class SongViewModule {}
