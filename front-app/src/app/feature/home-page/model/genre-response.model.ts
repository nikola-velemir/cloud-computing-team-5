import { HomeGenre } from './home-genre.model';

export interface GenresResponse {
  genres: HomeGenre[];
  lastToken?: string;
}
