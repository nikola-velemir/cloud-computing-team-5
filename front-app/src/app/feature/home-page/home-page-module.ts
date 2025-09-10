import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomePage } from './component/home-page/home-page';
import { FeedCard } from './component/feed-card/feed-card';
import { HomeSongCard } from './component/home-song-card/home-song-card';
import { HomeAlbumCard } from './component/home-album-card/home-album-card';
import { HomeArtistCard } from './component/home-artist-card/home-artist-card';
import { RouterLink } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HomeGenreCard } from './component/home-genre-card/home-genre-card';

@NgModule({
  declarations: [
    HomePage,
    FeedCard,
    HomeSongCard,
    HomeAlbumCard,
    HomeArtistCard,
    HomeGenreCard,
  ],
  imports: [CommonModule, RouterLink, HttpClientModule],
})
export class HomePageModule {}
