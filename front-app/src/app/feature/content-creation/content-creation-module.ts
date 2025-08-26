import { NgModule } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { ContentCreationForm } from './component/content-creation-form/content-creation-form.component';
import { FileUploadStep } from './component/step-one/file-upload-step/file-upload-step';
import { ArtistCard } from './component/step-three/artist-card/artist-card';
import { ArtistStep } from './component/step-three/artist-step/artist-step';
import { GenreCard } from './component/step-two/genre-card/genre-card.component';
import { MetadataForm } from './component/step-two/metadata-form/metadata-form';
import { NewAlbumForm } from './component/step-four/new-album-form/new-album-form';
import { SongList } from './component/step-two/song-list/song-list';
import { AlbumService } from './service/album-service';
import { ContentCreationApi } from './service/content-creation-api';
import { ContentCreationService } from './service/content-creation.service';
import { GenreService } from './service/genre-service';
import { PerformerService } from './service/performer-service';
import { AlbumCard } from './component/step-four/album-card/album-card';
import { AlbumForm } from './component/step-four/album-form/album-form';
import { SongListItem } from './component/step-two/song-list-item/song-list-item';

@NgModule({
  declarations: [
    ContentCreationForm,
    FileUploadStep,
    MetadataForm,
    ArtistCard,
    GenreCard,
    ArtistStep,
    AlbumCard,
    NewAlbumForm,
    AlbumForm,
    SongList,
    SongListItem,
  ],
  imports: [CommonModule, ReactiveFormsModule],
  exports: [AlbumCard, ContentCreationForm],
  providers: [
    DatePipe,
    ContentCreationService,
    ContentCreationApi,
    GenreService,
    PerformerService,
    AlbumService,
  ],
})
export class ContentCreationModule {}
