import { Component, ElementRef, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { loadAlbum } from '../../../content-audio-player/state/audio.actions';
import { GenrePreviewResponse } from '../../model/model';
import { GenreService } from '../../service/genre-service';
import { ReviewType, ReviewService } from '../../service/review-service';
import { switchMap } from 'rxjs';
import { SubscriptionService } from '../../../subscription/subscription.service';
import { EntityType } from '../../../subscription/model/EntityType.model';
import { ToastService } from '../../../../shared/toast/service/toast-service';

@Component({
  selector: 'app-genre-view',
  standalone: false,
  templateUrl: './genre-view.html',
  styleUrl: './genre-view.scss',
})
export class GenreView {
  genre: GenrePreviewResponse | null = null;
  reviewType = ReviewType.NONE;
  isSubscribed = false;
  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService,
    private activatedRoute: ActivatedRoute,
    private genreService: GenreService,
    private subscriptionService: SubscriptionService,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((p) => {
      const id = p['id'];
      this.genreService
        .getGenre(id)
        .pipe(
          switchMap((v) => {
            this.genre = v;
            console.log(this.genre);
            this.subscriptionService
              .isSubscribed(EntityType.GENRE, this.genre?.id)
              .subscribe((response) => {
                this.isSubscribed = response;
              });
            return this.reviewService.getReview(this.genre.id);
          })
        )
        .subscribe((v) => (this.reviewType = v.reviewType));
    });
  }

  playAlbum() {
    this.store.dispatch(loadAlbum({ albumId: 'this.genreId' }));
  }
  dislike() {
    const type =
      this.reviewType === ReviewType.DISLIKE
        ? ReviewType.NONE
        : ReviewType.DISLIKE;
    this.reviewService
      .setReview(this.genre!.id, type, this.genre?.imageUrl, this.genre?.name)
      .pipe(switchMap(() => this.reviewService.getReview(this.genre!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;
    this.reviewService
      .setReview(this.genre!.id, type, this.genre?.imageUrl, this.genre?.name)
      .pipe(switchMap(() => this.reviewService.getReview(this.genre!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;
    this.reviewService
      .setReview(this.genre!.id, type, this.genre?.imageUrl, this.genre?.name)
      .pipe(switchMap(() => this.reviewService.getReview(this.genre!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }
  @ViewChild('popover') popover!: ElementRef;
  @ViewChild('trigger') trigger!: ElementRef;
  positionPopover() {
    const rect = this.trigger.nativeElement.getBoundingClientRect();
    this.popover.nativeElement.style.top = rect.bottom + 10 + 'px';
    this.popover.nativeElement.style.left = rect.left - rect.width / 2 + 'px';
  }
  likesVisible = false;
  protected readonly ReviewType = ReviewType;

  toggleSubscription() {
    if (this.genre?.id) {
      if (this.isSubscribed) {
        this.subscriptionService
          .unsubscribe(EntityType.GENRE, this.genre?.id, this.genre.imageUrl)
          .subscribe((response) => {
            console.log(response);
            this.toast.success('Unsubscribed successfully');
            this.isSubscribed = response;
          });
      } else {
        this.subscriptionService
          .subscribe(EntityType.GENRE, this.genre?.id, this.genre?.name!,this.genre.imageUrl)
          .subscribe((response) => {
            console.log(response);
            this.toast.success('Subscribed successfully');
            this.isSubscribed = response;
          });
      }
    }
  }
}
