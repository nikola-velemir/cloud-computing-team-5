import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-confirm-dialog',
  imports: [],
  templateUrl: './confirm-dialog.html',
  styleUrl: './confirm-dialog.scss',
})
export class ConfirmDialog {
  @Input() message: string = 'Are you sure?';
  @Output() closed = new EventEmitter<boolean>();

  onConfirm() {
    this.closed.emit(true);
  }

  onCancel() {
    this.closed.emit(false);
  }
}
