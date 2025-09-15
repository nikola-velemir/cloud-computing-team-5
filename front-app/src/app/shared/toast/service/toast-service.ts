import { Injectable } from '@angular/core';
import {Toast, ToastType} from '../model/toast';
import {BehaviorSubject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  private toastsSubject = new BehaviorSubject<Toast[]>([]);
  toasts$ = this.toastsSubject.asObservable();

  private nextId() {
    return Math.random().toString(36).slice(2, 9);
  }

  private push(toast: Toast) {
    const current = this.toastsSubject.value;
    this.toastsSubject.next([...current, toast]);

    // auto remove
    if (toast.duration && toast.duration > 0) {
      setTimeout(() => this.remove(toast.id), toast.duration);
    }
  }

  show(message: string, type: ToastType = 'info', duration = 3000) {
    const t: Toast = { id: this.nextId(), message, type, duration };
    this.push(t);
    return t.id;
  }

  success(msg: string, duration = 4000) { return this.show(msg, 'success', duration); }
  info(msg: string, duration = 4000)    { return this.show(msg, 'info', duration); }
  warning(msg: string, duration = 6000) { return this.show(msg, 'warning', duration); }
  error(msg: string, duration = 6000)   { return this.show(msg, 'error', duration); }

  remove(id: string) {
    const next = this.toastsSubject.value.filter(t => t.id !== id);
    this.toastsSubject.next(next);
  }

  clear() { this.toastsSubject.next([]); }
}
