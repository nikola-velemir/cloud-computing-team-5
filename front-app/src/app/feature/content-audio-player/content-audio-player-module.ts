import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {AudioPlayer} from './component/audio-player/audio-player';
import {TimeFormatPipe} from './pipe/time-format-pipe';


@NgModule({
  declarations: [AudioPlayer, TimeFormatPipe],
  exports: [
    AudioPlayer
  ],
  imports: [
    CommonModule,

  ]
})
export class ContentAudioPlayerModule {
}
