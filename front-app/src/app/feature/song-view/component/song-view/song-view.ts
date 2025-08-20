import {Component, OnInit} from '@angular/core';
import {Store} from '@ngrx/store';
import {AppState} from '../../../../state/app-state';
import {loadTrack} from '../../../content-audio-player/state/audio.actions';
import {ReviewService, ReviewType} from '../../service/review.service';
import {switchMap} from 'rxjs';

@Component({
  selector: 'song-card',
  standalone: false,
  templateUrl: './song-view.html',
  styleUrl: './song-view.scss'
})
export class SongView implements OnInit {


  reviewType: ReviewType = ReviewType.NONE;
  private songId = 1;

  constructor(private store: Store<AppState>, private reviewService: ReviewService) {
  }

  ngOnInit(): void {
    this.reviewService.getReview(this.songId).subscribe(review => this.reviewType = review);

  }


  playSong() {
    this.store.dispatch(loadTrack({trackId: 10}))
  }

  dislike() {
    const type = this.reviewType === ReviewType.DISLIKE ? ReviewType.NONE : ReviewType.DISLIKE;
    this.reviewService.setReview(this.songId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.songId, type))
    ).subscribe(review => this.reviewType = review);
  }

  like() {
    const type = this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService.setReview(this.songId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.songId, type))
    ).subscribe(review => this.reviewType = review);
  }

  love() {
    const type = this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService.setReview(this.songId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.songId, type))
    ).subscribe(review => this.reviewType = review);
  }

  protected readonly ReviewType = ReviewType;
}
