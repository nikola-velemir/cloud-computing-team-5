import {Component} from '@angular/core';
import {RouterModule, RouterOutlet} from '@angular/router';
import {ContentCreationModule} from './feature/content-creation/content-creation-module';
import {NgxNotifier, NgxNotifierService} from 'ngx-notifier';
import {HttpClient, HttpClientModule} from '@angular/common/http';
import {SongViewModule} from './feature/song-view/song-view-module';
import {AlbumViewModule} from './feature/album-view/album-view-module';
import {PerformerViewModule} from './feature/performer-view/performer-view-module';
import {AudioApi} from './feature/content-audio-player/service/audio-api.service';
import {AudioService} from './feature/content-audio-player/service/audio-service';
import {ContentAudioPlayerModule} from './feature/content-audio-player/content-audio-player-module';

@Component({
  selector: 'app-root',
  imports: [
    ContentCreationModule,
    SongViewModule,
    AlbumViewModule,
    PerformerViewModule,
    RouterModule,
    NgxNotifier,
    HttpClientModule,
    ContentAudioPlayerModule,
  ],
  providers: [HttpClient,
    AudioApi, AudioService],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected title = 'front-app';

}
