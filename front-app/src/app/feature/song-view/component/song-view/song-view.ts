import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
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
import { DownloadService } from '../../service/download.service';

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
  isDownloading = false;

  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService,
    private activeRoute: ActivatedRoute,
    private songPreviewService: SongPreviewService,
    private downloadService: DownloadService
  ) {}

  ngOnInit(): void {
    this.activeRoute.params.subscribe((data) => {
      const id: string = data['id'];
      this.songPreviewService
        .getSongPreview(id)
        .pipe(
          switchMap((v) => {
            this.song = v;
            if (v.id) {
              console.log(this.isCached$);
              this.store.select(isTrackCached(v.id)).subscribe((x) => {
                this.isCached$ = x;
              });
              console.log(this.isCached$);
            }
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

  enableOffline() {
    this.store.dispatch(trackCached({ trackId: this.song?.id ?? '' }));
  }

  downloadSong() {
    if (this.song?.id) {
      this.isDownloading = true;
      this.downloadService.downloadSong(this.song?.id).finally(() => {
        this.isDownloading = false;
      });
    }
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
