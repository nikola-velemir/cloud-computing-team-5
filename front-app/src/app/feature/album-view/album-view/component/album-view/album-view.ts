import {Component, OnInit} from '@angular/core';
import {Store} from '@ngrx/store';
import {AppState} from '../../../../../state/app-state';
import {loadAlbum} from '../../../../content-audio-player/state/audio.actions';
import {ReviewService, ReviewType} from '../../../service/review.service';
import {switchMap} from 'rxjs';

@Component({
  selector: 'app-album.ts-view',
  standalone: false,
  templateUrl: './album-view.html',
  styleUrl: './album-view.scss'
})
export class AlbumView implements OnInit {
  private albumId = 1;
  public reviewType = ReviewType.NONE;

  constructor(private store: Store<AppState>, private reviewService: ReviewService) {
  }

  ngOnInit(): void {
    this.reviewService.getReview(this.albumId).subscribe(review => this.reviewType = review);
  }

  playAlbum() {
    this.store.dispatch(loadAlbum({albumId: this.albumId}))
  }
  dislike() {
    const type = this.reviewType === ReviewType.DISLIKE ? ReviewType.NONE : ReviewType.DISLIKE;
    this.reviewService.setReview(this.albumId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.albumId, type))
    ).subscribe(review => this.reviewType = review);
  }

  like() {
    const type = this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService.setReview(this.albumId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.albumId, type))
    ).subscribe(review => this.reviewType = review);
  }

  love() {
    const type = this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService.setReview(this.albumId, type).pipe(
      switchMap(() => this.reviewService.getReview(this.albumId, type))
    ).subscribe(review => this.reviewType = review);
  }

  protected readonly ReviewType = ReviewType;
}
