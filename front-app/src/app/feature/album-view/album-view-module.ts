import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlbumView } from './album-view/component/album-view/album-view';
import { PerformerCard } from './album-view/component/performer-card/performer-card';
import { SongItem } from './album-view/component/song-item/song-item';
import { ReviewService } from './service/review.service';
import { RouterLink } from '@angular/router';
import { AlbumPreviewService } from './service/album-preview';

@NgModule({
  declarations: [AlbumView, PerformerCard, SongItem],
  imports: [CommonModule, RouterLink],
  providers: [ReviewService, AlbumPreviewService],
  exports: [AlbumView],
})
export class AlbumViewModule {}
