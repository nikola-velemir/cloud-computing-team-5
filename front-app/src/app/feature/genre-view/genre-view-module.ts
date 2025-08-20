import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {GenreView} from './component/genre-view/genre-view';
import {AlbumCard} from './component/album-card/album-card';
import {PerformerCard} from './component/performer-card/performer-card';
import {SongCard} from './component/song-card/song-card';
import {RouterLink} from '@angular/router';


@NgModule({
  declarations: [GenreView,AlbumCard,PerformerCard],
  imports: [
    CommonModule,
    SongCard,
    RouterLink
  ], exports: [GenreView],
})
export class GenreViewModule {
}
