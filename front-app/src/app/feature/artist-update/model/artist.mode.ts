import { Genre } from './genre.model';

export interface Artist {
  id: string;
  name: string;
  biography: string;
  genres: Genre[];
}
