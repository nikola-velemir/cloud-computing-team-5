import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../../state/app-state';
import { loadAlbum } from '../../../../content-audio-player/state/audio.actions';
import { ReviewService, ReviewType } from '../../../service/review.service';
import { switchMap } from 'rxjs';
import { AlbumPreviewService } from '../../../service/album-preview';
import { ActivatedRoute } from '@angular/router';
import { AlbumViewResponse } from '../../../model/album-view-response';

@Component({
  selector: 'app-album.ts-view',
  standalone: false,
  templateUrl: './album-view.html',
  styleUrl: './album-view.scss',
})
export class AlbumView implements OnInit {
  private albumId = 1;
  public reviewType = ReviewType.NONE;
  album: AlbumViewResponse | null = null;
  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService,
    private albumService: AlbumPreviewService,
    private activeRoute: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.activeRoute.params.subscribe((data) => {
      const id = data['id'];
      this.albumService.getAlbumForView(id).subscribe((v) => {
        console.log(v);
        this.album = v;
      });
    });

    this.reviewService
      .getReview(this.albumId)
      .subscribe((review) => (this.reviewType = review));
  }

  playAlbum() {
    this.store.dispatch(loadAlbum({ albumId: this.album?.id ?? '' }));
  }
  dislike() {
    const type =
      this.reviewType === ReviewType.DISLIKE
        ? ReviewType.NONE
        : ReviewType.DISLIKE;
    this.reviewService
      .setReview(this.albumId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.albumId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    this.reviewService
      .setReview(this.albumId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.albumId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    this.reviewService
      .setReview(this.albumId, type)
      .pipe(switchMap(() => this.reviewService.getReview(this.albumId, type)))
      .subscribe((review) => (this.reviewType = review));
  }

  protected readonly ReviewType = ReviewType;
}
