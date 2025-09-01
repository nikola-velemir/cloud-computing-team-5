import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DiscoverPage } from './component/discover-page/discover-page';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [DiscoverPage],
  imports: [CommonModule, FormsModule],
})
export class DiscoverPageModule {}
