import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SongView} from './component/song-view/song-view';
import {AlbumCard} from './component/album-card/album-card';
import {PerformerCard} from './component/performer-card/performer-card';
import {RouterLink} from "@angular/router";
import {ReviewService} from './service/review.service';


@NgModule({
  declarations: [SongView, AlbumCard, PerformerCard],
  imports: [
    CommonModule,
    RouterLink
  ],
  providers: [ReviewService],
  exports: [SongView]
})
export class SongViewModule {
}
