import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SongView} from './component/song-view/song-view';
import {AlbumCard} from './component/album-card/album-card';
import {PerformerCard} from './component/performer-card/performer-card';


@NgModule({
  declarations: [SongView, AlbumCard, PerformerCard],
  imports: [
    CommonModule
  ]
})
export class SongViewModule {
}
