import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ReviewService, ReviewType } from '../../service/review.service';
import { switchMap } from 'rxjs';
import { PerformerViewService } from '../../service/performer-view-service';
import { ActivatedRoute } from '@angular/router';
import { ArtistViewResponse } from '../../model/artist-view-response';

@Component({
  selector: 'app-performer-view',
  standalone: false,
  templateUrl: './performer-view.html',
  styleUrl: './performer-view.scss',
})
export class PerformerView implements OnInit {
  protected readonly ReviewType = ReviewType;
  reviewType: ReviewType = ReviewType.NONE;

  artist: ArtistViewResponse | null = null;
  constructor(
    private readonly reviewService: ReviewService,
    private readonly performerViewSerive: PerformerViewService,
    private readonly activeRoute: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.activeRoute.params.subscribe((data) => {
      const id = data['id'];
      this.performerViewSerive
        .getPerformer(id)
        .pipe(
          switchMap((v) => {
            this.artist = v;
            return this.reviewService.getReview(this.artist!.id);
          })
        )
        .subscribe((review) => {
          console.log(review);
          this.reviewType = review.reviewType;
        });
    });
  }

  dislike() {
    const type =
      this.reviewType === ReviewType.DISLIKE
        ? ReviewType.NONE
        : ReviewType.DISLIKE;
    this.reviewService
      .setReview(this.artist!.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.artist!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService
      .setReview(this.artist!.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.artist!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService
      .setReview(this.artist!.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.artist!.id)))
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
}
