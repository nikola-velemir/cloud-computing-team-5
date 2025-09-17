import { Component } from '@angular/core';
import {User} from '../../../../infrastructure/auth/model/user.mode';
import {UserRole} from '../../../../infrastructure/auth/model/user-role.model';
import {Observable, of} from 'rxjs';
import {AsyncPipe, DatePipe, NgForOf} from '@angular/common';
import {SubscriptionResponse} from '../../model/SubscriptionResponse';
import {AuthService} from '../../../../infrastructure/auth/service/auth.service';
import {SubscriptionService} from '../../subscription.service';
import {ToastService} from '../../../../shared/toast/service/toast-service';

@Component({
  selector: 'app-subscribe-list',
  imports: [
    DatePipe,
    NgForOf,
  ],
  templateUrl: './subscribe-list.html',
  styleUrl: './subscribe-list.scss'
})
export class SubscribeList {
  user:User| null = null

  subscriptions: SubscriptionResponse[] = []

  constructor(private authService:AuthService, private subsService:SubscriptionService,
              private toastr:ToastService) { }

  ngOnInit(): void {
    this.user = this.authService.getUser();
    this.getSubs();
  }

  getSubs(){
    this.subsService.getSubscribesByUser().subscribe({
      next: (subs) => {
        this.subscriptions = subs;
      },
      error: (err) => {
        this.toastr.error("Fetching subscriptions failed.")
      }
      }
    )
  }
}
