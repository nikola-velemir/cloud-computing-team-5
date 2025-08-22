import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomePage } from './component/home-page/home-page';
import { DiscoverPage } from './component/discover-page/discover-page';
import { GenreViewModule } from '../genre-view/genre-view-module';
import { RouterModule } from '@angular/router';
import { FeedCard } from './component/feed-card/feed-card';

@NgModule({
  declarations: [HomePage, DiscoverPage, FeedCard],
  imports: [CommonModule, GenreViewModule, RouterModule],
})
export class HomePageModule {}
