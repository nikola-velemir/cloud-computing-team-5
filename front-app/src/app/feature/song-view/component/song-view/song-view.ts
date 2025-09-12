import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import {
  loadTrack,
  trackCached,
} from '../../../content-audio-player/state/audio.actions';
import { ReviewService, ReviewType } from '../../service/review.service';
import { Observable, switchMap } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { SongPreviewService } from '../../service/song-preview';
import { SongViewResponse } from '../../model/song-view-response';
import { isTrackCached } from '../../../content-audio-player/state/audio.selectors';

@Component({
  selector: 'song-card',
  standalone: false,
  templateUrl: './song-view.html',
  styleUrl: './song-view.scss',
})
export class SongView implements OnInit {
  reviewType: ReviewType = ReviewType.NONE;
  private songId = 1;
  song: SongViewResponse | null = null;
  isCached$!: Observable<boolean>;

  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService,
    private activeRoute: ActivatedRoute,
    private songPreviewService: SongPreviewService
  ) {}

  ngOnInit(): void {
    this.activeRoute.params.subscribe((data) => {
      const id: string = data['id'];
      this.songPreviewService.getSongPreview(id).subscribe((v) => {
        this.song = v;
        if (v.id) {
          console.log(this.isCached$);
          this.store.select(isTrackCached(v.id)).subscribe((x) => {
            this.isCached$ = x;
          });
          console.log(this.isCached$);
        }
      });
    });
    this.reviewService
      .getReview(this.songId)
      .subscribe((review) => (this.reviewType = review));
  }

  playSong() {
    this.store.dispatch(loadTrack({ trackId: this.song?.id ?? '' }));
  }

  enableOffline() {
    this.store.dispatch(trackCached({ trackId: this.song?.id ?? '' }));
  }

  dislike() {
    const type =
      this.reviewType === ReviewType.DISLIKE
        ? ReviewType.NONE
        : ReviewType.DISLIKE;
    this.reviewService
      .setReview(this.songId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.songId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService
      .setReview(this.songId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.songId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService
      .setReview(this.songId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.songId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  protected readonly ReviewType = ReviewType;
}
