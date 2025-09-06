import { Song } from './song.model';

export interface SongsResponse {
  songs: Song[];
  totalPages: number;
}
