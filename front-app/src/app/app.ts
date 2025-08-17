import {Component} from '@angular/core';
import {RouterModule, RouterOutlet} from '@angular/router';
import {ContentCreationModule} from './feature/content-creation/content-creation-module';
import {NgxNotifier, NgxNotifierService} from 'ngx-notifier';
import {HttpClient, HttpClientModule} from '@angular/common/http';
import {SongViewModule} from './feature/song-view/song-view-module';
import {AlbumViewModule} from './feature/album-view/album-view-module';
import {PerformerViewModule} from './feature/performer-view/performer-view-module';

@Component({
  selector: 'app-root',
  imports: [ContentCreationModule, SongViewModule, AlbumViewModule, PerformerViewModule, RouterModule, NgxNotifier, HttpClientModule],
  providers: [HttpClient],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected title = 'front-app';
}
