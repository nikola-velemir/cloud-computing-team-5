import { Component } from '@angular/core';
import {RouterModule, RouterOutlet} from '@angular/router';
import {SongCreationModule} from './feature/content-creation/song-creation-module';
import {NgxNotifier, NgxNotifierService} from 'ngx-notifier';

@Component({
  selector: 'app-root',

  imports: [SongCreationModule, RouterModule, NgxNotifier],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected title = 'front-app';
}
