import { Component } from '@angular/core';
import { ReviewType } from '../../service/review-service';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { ReviewService } from '../../../album-view/service/review.service';
import { loadAlbum } from '../../../content-audio-player/state/audio.actions';
import { switchMap } from 'rxjs';

@Component({
  selector: 'app-genre-view',
  standalone: false,
  templateUrl: './genre-view.html',
  styleUrl: './genre-view.scss',
})
export class GenreView {
  private genreId = 21;
  reviewType = ReviewType.NONE;
  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService
  ) {}

  ngOnInit(): void {
    this.reviewService
      .getReview(this.genreId)
      .subscribe((review) => (this.reviewType = review));
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
      .setReview(this.genreId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.genreId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService
      .setReview(this.genreId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.genreId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService
      .setReview(this.genreId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.genreId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  protected readonly ReviewType = ReviewType;
}
