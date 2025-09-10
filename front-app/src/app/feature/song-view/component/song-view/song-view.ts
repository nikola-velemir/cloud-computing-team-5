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
      this.songPreviewService.getSongPreview(id).subscribe((v) => {
        this.song = v;
        console.log(this.song);
      });
    });
    this.reviewService
      .getReview(this.songId)
      .subscribe((review) => (this.reviewType = review));
  }

  playSong() {
    this.store.dispatch(loadTrack({ trackId: this.song?.id ?? '' }));
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
