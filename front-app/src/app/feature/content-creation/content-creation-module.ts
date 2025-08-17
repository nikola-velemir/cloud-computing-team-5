import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ContentCreationForm} from './component/content-creation-form/content-creation-form.component';
import {FileUploadStep} from './component/file-upload-step/file-upload-step';
import {MetadataForm} from './component/metadata-form/metadata-form';
import {ReactiveFormsModule} from '@angular/forms';
import {AuthorCard} from './component/author-card/author-card';
import {GenreCard} from './component/genre-card/genre-card.component';
import {PerformerAlbumStep} from './component/performer-album-step/performer-album-step';
import {AlbumCard} from './component/album-card/album-card';
import {ContentCreationService} from './service/content-creation.service';
import {SongList} from './component/song-list/song-list';
import {NewAlbumForm} from './component/new-album-form/new-album-form';
import {ContentCreationApi} from './service/content-creation-api';


@NgModule({
  declarations: [
    ContentCreationForm, FileUploadStep, MetadataForm, AuthorCard, GenreCard, PerformerAlbumStep, AlbumCard, NewAlbumForm
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    SongList,
  ],
  exports: [
    AlbumCard
  ],
  providers: [ContentCreationService, ContentCreationApi]
})
export class ContentCreationModule {
}
