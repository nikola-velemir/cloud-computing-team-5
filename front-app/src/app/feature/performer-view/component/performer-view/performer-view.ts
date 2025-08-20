import {Component, OnInit} from '@angular/core';
import {ReviewService, ReviewType} from '../../service/review.service';
import {switchMap} from 'rxjs';


@Component({
  selector: 'app-performer-view',
  standalone: false,
  templateUrl: './performer-view.html',
  styleUrl: './performer-view.scss'
})
export class PerformerView implements OnInit {
  performerId: number = 201;

  protected readonly ReviewType = ReviewType;
  reviewType: ReviewType = ReviewType.NONE;

  constructor(private readonly reviewService: ReviewService) {
  }


  ngOnInit(): void {
    this.reviewService.getReview(this.performerId).subscribe(review => this.reviewType = review);
  }


  dislike() {
    const type = this.reviewType === ReviewType.DISLIKE ? ReviewType.NONE : ReviewType.DISLIKE;
    this.reviewService.setReview(this.performerId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.performerId, type))
    ).subscribe(review => this.reviewType = review);
  }

  like() {
    const type = this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService.setReview(this.performerId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.performerId, type))
    ).subscribe(review => this.reviewType = review);
  }

  love() {
    const type = this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService.setReview(this.performerId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.performerId, type))
    ).subscribe(review => this.reviewType = review);
  }
}
