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
      case 'success': return 'bg-green-50 text-green-800 border border-green-100';
      case 'warning': return 'bg-yellow-50 text-yellow-800 border border-yellow-100';
      case 'error':   return 'bg-red-50 text-red-800 border border-red-100';
      default:        return 'bg-primary-50 text-primary-800 border border-primary-100';
    }
  }
}
