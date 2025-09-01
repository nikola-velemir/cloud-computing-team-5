import { HomeSong } from './home-song.mode';

export interface SongsResponse {
  songs: HomeSong[];
  lastToken?: string;
}
