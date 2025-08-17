import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {AlbumView} from './album-view/component/album-view/album-view';
import {PerformerCard} from './album-view/component/performer-card/performer-card';
import {SongItem} from './album-view/component/song-item/song-item';


@NgModule({
  declarations: [AlbumView, PerformerCard, SongItem],
  imports: [
    CommonModule
  ]
})
export class AlbumViewModule {
}
