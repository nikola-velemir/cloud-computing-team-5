import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ContentCreationModule } from './feature/content-creation/content-creation-module';
import { NgxNotifier } from 'ngx-notifier';
import {
  HTTP_INTERCEPTORS,
  HttpClient,
  HttpClientModule,
} from '@angular/common/http';
import { SongViewModule } from './feature/song-view/song-view-module';
import { AlbumViewModule } from './feature/album-view/album-view-module';
import { PerformerViewModule } from './feature/performer-view/performer-view-module';
import { AudioApi } from './feature/content-audio-player/service/audio-api.service';
import { AudioService } from './feature/content-audio-player/service/audio-service';
import { ContentAudioPlayerModule } from './feature/content-audio-player/content-audio-player-module';
import { GenreViewModule } from './feature/genre-view/genre-view-module';
import { GenreCreationModule } from './feature/category-creation/genre-creation-module';
import { NavModule } from './feature/nav/nav-module';
import { HomePageModule } from './feature/home-page/home-page-module';
import { LoginModule } from './feature/login/login-module';

import { AuthInterceptor } from './infrastructure/interceptor/AuthInterceptor';
import { ToastContainer } from './shared/toast/toast-container/toast-container';
import { DiscoverPageModule } from './feature/discover-page/discover-page-module';

@Component({
  selector: 'app-root',
  imports: [
    ContentCreationModule,
    SongViewModule,
    AlbumViewModule,
    GenreViewModule,
    PerformerViewModule,
    RouterModule,
    NgxNotifier,
    HttpClientModule,
    ContentAudioPlayerModule,
    GenreCreationModule,
    NavModule,
    HomePageModule,
    LoginModule,
    ToastContainer,
    DiscoverPageModule,
  ],
  providers: [HttpClient, AudioApi, AudioService],

  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected title = 'songify-app';
}
