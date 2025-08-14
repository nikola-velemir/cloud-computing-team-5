import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SongCreationForm} from './component/content-creation-form/song-creation-form.component';
import {FileUploadStep} from './component/file-upload-step/file-upload-step';
import {MetadataForm} from './component/metadata-form/metadata-form';
import {ReactiveFormsModule} from '@angular/forms';
import {AuthorCard} from './component/author-card/author-card';
import {GenreCard} from './component/genre-card/genre-card.component';
import {PerformerAlbumStep} from './component/performer-album-step/performer-album-step';
import {AlbumCard} from './component/album-card/album-card';
import {ContentCreationService} from './service/content-creation.service';


@NgModule({
  declarations: [
    SongCreationForm, FileUploadStep, MetadataForm, AuthorCard, GenreCard, PerformerAlbumStep,AlbumCard
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
  ],
  providers: [ContentCreationService]
})
export class SongCreationModule {
}
