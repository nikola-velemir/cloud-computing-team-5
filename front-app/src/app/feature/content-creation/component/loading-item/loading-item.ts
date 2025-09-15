import { Component, Input } from '@angular/core';

export interface LoadingItemModel {
  name: string;
  statusMessage: string;
  status: 'inProgress' | 'done' | 'failed';
}

@Component({
  selector: 'content-creation-loading-item',
  standalone: false,
  templateUrl: './loading-item.html',
  styleUrl: './loading-item.scss',
})
export class LoadingItem {
  @Input() name: string = '';
  @Input() statusMessage: string = '';
  @Input() status: 'inProgress' | 'done' | 'failed' = 'inProgress';
}
