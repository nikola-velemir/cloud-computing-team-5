import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContentCreationForm } from './component/content-creation-form/content-creation-form.component';
import { MetadataForm } from './component/step-two/metadata-form/metadata-form';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthorCard } from './component/step-three/author-card/author-card';
import { GenreCard } from './component/step-two/genre-card/genre-card.component';
import { PerformerAlbumStep } from './component/step-three/performer-album-step/performer-album-step';
import { AlbumCard } from './component/step-three/album-card/album-card';
import { ContentCreationService } from './service/content-creation.service';
import { SongList } from './component/step-two/song-list/song-list';
import { NewAlbumForm } from './component/step-three/new-album-form/new-album-form';
import { ContentCreationApi } from './service/content-creation-api';
import { FileUploadStep } from './component/step-one/file-upload-step/file-upload-step';

@NgModule({
  declarations: [
    ContentCreationForm,
    FileUploadStep,
    MetadataForm,
    AuthorCard,
    GenreCard,
    PerformerAlbumStep,
    AlbumCard,
    NewAlbumForm,
  ],
  imports: [CommonModule, ReactiveFormsModule, SongList],
  exports: [AlbumCard],
  providers: [ContentCreationService, ContentCreationApi],
})
export class ContentCreationModule {}
