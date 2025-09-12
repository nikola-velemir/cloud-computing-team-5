import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { environment } from '../../../../environments/environement';

export enum ReviewType {
  NONE = 'NONE',
  DISLIKE = 'DISLIKE',
  LIKE = 'LIKE',
  LOVE = 'LOVE',
}

@Injectable({ providedIn: 'root' })
export class ReviewService {
  private readonly BASE_URL = environment.apiUrl + '/content-reviews/artists';
  constructor(private readonly http: HttpClient) {}

  setReview(artistId: string, reviewType: ReviewType) {
    return this.http.put(this.BASE_URL, { artistId, reviewType });
  }

  getReview(artistId: string) {
    return this.http.get<{ reviewType: ReviewType }>(
      `${this.BASE_URL}/${artistId}`
    );
  }
}
