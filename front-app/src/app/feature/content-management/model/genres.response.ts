import { Genre } from './genre.model';

export interface GenresResponse {
  genres: Genre[];
  lastToken?: string;
}
