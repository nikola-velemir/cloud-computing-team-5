import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { loadTrack } from '../../../content-audio-player/state/audio.actions';
import { ReviewService, ReviewType } from '../../service/review.service';
import { switchMap } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { SongPreviewService } from '../../service/song-preview';
import { SongViewResponse } from '../../model/song-view-response';

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
  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService,
    private activeRoute: ActivatedRoute,
    private songPreviewService: SongPreviewService
  ) {}

  ngOnInit(): void {
    this.activeRoute.params.subscribe((data) => {
      const id: string = data['id'];
      this.songPreviewService
        .getSongPreview(id)
        .pipe(
          switchMap((v) => {
            this.song = v;
            return this.reviewService.getReview(this.song.id);
          })
        )

        .subscribe((review) => {
          console.log(review);
          this.reviewType = review.reviewType;
        });
    });
  }

  playSong() {
    this.store.dispatch(loadTrack({ trackId: this.song?.id ?? '' }));
  }

  dislike() {
    const type =
      this.reviewType === ReviewType.DISLIKE
        ? ReviewType.NONE
        : ReviewType.DISLIKE;
    if (!this.song) return;
    this.reviewService
      .setReview(this.song.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.song!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;
    if (!this.song) return;
    this.reviewService
      .setReview(this.song.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.song!.id)))
      .subscribe((review) => (this.reviewType = review.reviewType));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;
    if (!this.song) return;
    this.reviewService
      .setReview(this.song.id, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.song!.id)))
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
}
