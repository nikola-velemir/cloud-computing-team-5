import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { environment } from '../../../../environments/environement';
import { HttpClient } from '@angular/common/http';

export enum ReviewType {
  NONE = 'NONE',
  DISLIKE = 'DISLIKE',
  LIKE = 'LIKE',
  LOVE = 'LOVE',
}

@Injectable({ providedIn: 'root' })
export class ReviewService {
  private readonly BASE_URL = environment.apiUrl + '/content-reviews/albums';
  constructor(private readonly http: HttpClient) {}

  setReview(albumId: string, reviewType: ReviewType, coverPath?: string, name?:string) {
    return this.http.put(this.BASE_URL, { albumId, reviewType, CoverPath:coverPath, NameEntity:name });
  }

  getReview(albumId: string) {
    return this.http.get<{ reviewType: ReviewType }>(
      `${this.BASE_URL}/${albumId}`
    );
  }
}
