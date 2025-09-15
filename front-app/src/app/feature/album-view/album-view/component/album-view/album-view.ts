import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../../state/app-state';
import { loadAlbum } from '../../../../content-audio-player/state/audio.actions';
import { ReviewService, ReviewType } from '../../../service/review.service';
import { switchMap } from 'rxjs';
import { AlbumPreviewService } from '../../../service/album-preview';
import { ActivatedRoute } from '@angular/router';
import { AlbumViewResponse } from '../../../model/album-view-response';
import { SubscriptionService } from '../../../../subscription/subscription.service';
import { EntityType } from '../../../../subscription/model/EntityType.model';
import { ToastService } from '../../../../../shared/toast/service/toast-service';

@Component({
  selector: 'app-album.ts-view',
  standalone: false,
  templateUrl: './album-view.html',
  styleUrl: './album-view.scss',
})
export class AlbumView implements OnInit {
  private albumId = 1;
  public reviewType = ReviewType.NONE;
  album: AlbumViewResponse | null = null;
  isSubscribed = false;

  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService,
    private albumService: AlbumPreviewService,
    private activeRoute: ActivatedRoute,
    private subscriptionService: SubscriptionService,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.activeRoute.params.subscribe((data) => {
      const id = data['id'];
      this.albumService
        .getAlbumForView(id)
        .pipe(
          switchMap((v) => {
            this.album = v;
            this.subscriptionService
              .isSubscribed(EntityType.ALBUM, this.album?.id)
              .subscribe((response) => {
                this.isSubscribed = response;
              });
            return this.reviewService.getReview(this.album!.id);
          })
        )
        .subscribe((review) => (this.reviewType = review.reviewType));
    });
  }

  playAlbum() {
    this.store.dispatch(loadAlbum({ albumId: this.album?.id ?? '' }));
  }
  dislike() {
    const type =
      this.reviewType === ReviewType.DISLIKE
        ? ReviewType.NONE
        : ReviewType.DISLIKE;
    this.reviewService
      .setReview(this.album!.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.album!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService
      .setReview(this.album!.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.album!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService
      .setReview(this.album!.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.album!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }
  likesVisible = false;
  @ViewChild('popover') popover!: ElementRef;
  @ViewChild('trigger') trigger!: ElementRef;
  positionPopover() {
    const rect = this.trigger.nativeElement.getBoundingClientRect();
    this.popover.nativeElement.style.top = rect.bottom + 10 + 'px';
    this.popover.nativeElement.style.left = rect.left - rect.width / 2 + 'px';
  }
  protected readonly ReviewType = ReviewType;

  toggleSubscription() {
    if (this.album) {
      if (this.isSubscribed) {
        this.subscriptionService
          .unsubscribe(EntityType.ALBUM, this.album?.id)
          .subscribe((response) => {
            this.isSubscribed = response;
            this.toast.success('Unsubscribed successfully');
          });
      } else {
        this.subscriptionService
          .subscribe(EntityType.ALBUM, this.album?.id)
          .subscribe((response) => {
            this.isSubscribed = response;
            this.toast.success('Subscribed successfully');
          });
      }
    }
  }
}
