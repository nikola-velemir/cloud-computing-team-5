import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomePage } from './component/home-page/home-page';
import { DiscoverPage } from './component/discover-page/discover-page';

@NgModule({
  declarations: [HomePage, DiscoverPage],
  imports: [CommonModule],
})
export class HomePageModule {}
