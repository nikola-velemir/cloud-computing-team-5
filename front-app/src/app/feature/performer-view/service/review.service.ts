import { Injectable } from '@angular/core';
import {of} from 'rxjs';

export enum ReviewType {
  NONE,
  DISLIKE,
  LIKE,
  LOVE
}

@Injectable({providedIn: 'root'})
export class ReviewService {

  constructor() {
  }

  setReview(contentId: number, review: ReviewType) {
    return of(review);
  }

  getReview(albumId: number, review: ReviewType = ReviewType.NONE) {
    return of(review)
  }

}
