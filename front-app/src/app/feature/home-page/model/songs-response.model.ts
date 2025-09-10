import { HomeSong } from './home-song.model';

export interface SongsResponse {
  songs: HomeSong[];
  lastToken?: string;
}
