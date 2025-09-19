import { Component } from '@angular/core';

@Component({
  selector: 'app-content-list',
  standalone: false,
  templateUrl: './content-list.html',
  styleUrl: './content-list.scss',
})
export class ContentList {
  viewMode: any;
  loading: any;
  showCreate: any;
  artists: any;
  prevDisabled: any;

  showSongs() {
    this.viewMode = 'songs';
  }
  showAlbums() {
    this.viewMode = 'albums';
  }

  showGenres() {
    this.viewMode = 'genres';
  }
}
