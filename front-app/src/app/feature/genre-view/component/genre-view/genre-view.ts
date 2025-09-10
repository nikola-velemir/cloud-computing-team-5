import { Component, ElementRef, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../state/app-state';
import { loadAlbum } from '../../../content-audio-player/state/audio.actions';
import { GenrePreviewResponse } from '../../model/model';
import { GenreService } from '../../service/genre-service';
import { ReviewType, ReviewService } from '../../service/review-service';

@Component({
  selector: 'app-genre-view',
  standalone: false,
  templateUrl: './genre-view.html',
  styleUrl: './genre-view.scss',
})
export class GenreView {
  genre: GenrePreviewResponse | null = null;
  reviewType = ReviewType.NONE;
  constructor(
    private store: Store<AppState>,
    private reviewService: ReviewService,
    private activatedRoute: ActivatedRoute,
    private genreService: GenreService
  ) {}

  ngOnInit(): void {
    // this.reviewService
    //   .getReview(this.genreId)
    //   .subscribe((review) => (this.reviewType = review));
    this.activatedRoute.params.subscribe((p) => {
      const id = p['id'];
      this.genreService.getGenre(id).subscribe((v) => (this.genre = v));
    });
  }

  playAlbum() {
    this.store.dispatch(loadAlbum({ albumId: 'this.genreId' }));
  }
  dislike() {
    const type =
      this.reviewType === ReviewType.DISLIKE
        ? ReviewType.NONE
        : ReviewType.DISLIKE;
    // this.reviewService
    //   .setReview(this.genreId, type)
    //   .pipe(switchMap(() => this.reviewService.getReview(this.genreId, type)))
    //   .subscribe((review) => (this.reviewType = review));
  }

  like() {
    const type =
      this.reviewType === ReviewType.LIKE ? ReviewType.NONE : ReviewType.LIKE;

    // this.reviewService
    //   .setReview(this.genreId, type)
    //   .pipe(switchMap(() => this.reviewService.getReview(this.genreId, type)))
    //   .subscribe((review) => (this.reviewType = review));
  }

  love() {
    const type =
      this.reviewType === ReviewType.LOVE ? ReviewType.NONE : ReviewType.LOVE;

    // this.reviewService
    //   .setReview(this.genreId, type)
    //   .pipe(switchMap(() => this.reviewService.getReview(this.genreId, type)))
    //   .subscribe((review) => (this.reviewType = review));
  }
  @ViewChild('popover') popover!: ElementRef;
  @ViewChild('trigger') trigger!: ElementRef;
  positionPopover() {
    const rect = this.trigger.nativeElement.getBoundingClientRect();
    this.popover.nativeElement.style.top = rect.bottom + 10 + 'px';
    this.popover.nativeElement.style.left = rect.left - rect.width / 2 + 'px';
  }
  likesVisible = false;
  protected readonly ReviewType = ReviewType;
}
