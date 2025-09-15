import { Component } from '@angular/core';
import {ToastService} from '../service/toast-service';
import {Subscription} from 'rxjs';
import {Toast} from '../model/toast';
import {NgClass, NgForOf} from '@angular/common';

@Component({
  selector: 'app-toast-container',
  imports: [
    NgClass,
    NgForOf
  ],
  templateUrl: './toast-container.html',
  styleUrl: './toast-container.scss'
})
export class ToastContainer {
  toasts: Toast[] = [];
  sub: Subscription;

  constructor(private toastService: ToastService) {
    this.sub = this.toastService.toasts$.subscribe(list => this.toasts = list);
  }

  ngOnDestroy() { this.sub?.unsubscribe(); }

  close(id: string) { this.toastService.remove(id); }

  toastClass(type: string) {

    switch (type) {
      case 'success':
        return 'bg-green-200 text-green-900 border border-green-300';
      case 'warning':
        return 'bg-yellow-200 text-yellow-900 border border-yellow-300';
      case 'error':
        return 'bg-red-200 text-red-900 border border-red-300';
      default:
        return 'bg-primary-400 text-primary-900 border border-primary-500';
    }

  }
}
