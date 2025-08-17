import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {PerformerView} from './component/performer-view/performer-view';
import {AlbumCard} from './component/album-card/album-card';
import {SongItem} from './component/song-item/song-item';


@NgModule({
  declarations: [PerformerView, AlbumCard,SongItem],
  imports: [
    CommonModule
  ]
})
export class PerformerViewModule {
}
