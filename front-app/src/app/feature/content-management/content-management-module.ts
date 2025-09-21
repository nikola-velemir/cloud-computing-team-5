import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContentList } from './component/content-list/content-list';
import { AlbumsList } from './component/albums-list/albums-list';
import { SongList } from './component/song-list/song-list';
import { ArtistForm } from '../artist-creation/component/artist-form/artist-form';
import { ConfirmDialog } from '../../shared/component/confirm-dialog/confirm-dialog';
import { GenreList } from './component/genre-list/genre-list';

@NgModule({
  declarations: [ContentList, AlbumsList, SongList, GenreList],
  imports: [CommonModule, ArtistForm, ConfirmDialog],
})
export class ContentManagementModule {}
