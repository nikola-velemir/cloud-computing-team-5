import { Component } from '@angular/core';
import {RouterLink} from '@angular/router';
import {ArtistForm} from '../artist-form/artist-form';
import {NgIf} from '@angular/common';

@Component({
  selector: 'app-artist-list',
  imports: [
    ArtistForm,
    NgIf
  ],
  templateUrl: './artist-list.html',
  styleUrl: './artist-list.scss'
})
export class ArtistList {
  showCreate = false;

  toggleCreate(): void {
    this.showCreate = !this.showCreate;
  }
}
