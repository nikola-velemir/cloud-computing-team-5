import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AudioPlayer } from './component/audio-player/audio-player';
import { TimeFormatPipe } from './pipe/time-format-pipe';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [AudioPlayer, TimeFormatPipe],
  exports: [AudioPlayer],
  imports: [CommonModule, RouterModule],
})
export class ContentAudioPlayerModule {}
