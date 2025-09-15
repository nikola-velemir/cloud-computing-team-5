import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environement';

export enum ReviewType {
  NONE = 'NONE',
  DISLIKE = 'DISLIKE',
  LIKE = 'LIKE',
  LOVE = 'LOVE',
}

@Injectable({
  providedIn: 'root',
})
export class ReviewService {
  private readonly BASE_URL = environment.apiUrl + '/content-reviews/genres';
  constructor(private readonly http: HttpClient) {}

  setReview(genreId: string, reviewType: ReviewType) {
    return this.http.put(this.BASE_URL, { genreId, reviewType });
  }

  getReview(genreId: string) {
    return this.http.get<{ reviewType: ReviewType }>(
      `${this.BASE_URL}/${genreId}`
    );
  }
}
