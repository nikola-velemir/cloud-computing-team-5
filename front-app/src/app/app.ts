import {Component} from '@angular/core';
import {RouterModule, RouterOutlet} from '@angular/router';
import {ContentCreationModule} from './feature/content-creation/content-creation-module';
import {NgxNotifier, NgxNotifierService} from 'ngx-notifier';
import {HttpClient, HttpClientModule} from '@angular/common/http';

@Component({
  selector: 'app-root',
  imports: [ContentCreationModule, RouterModule, NgxNotifier, HttpClientModule],
  providers: [HttpClient],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected title = 'front-app';
}
