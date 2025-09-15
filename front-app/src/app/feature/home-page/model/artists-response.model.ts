import { HomeArtist } from './home-artist.model';

export interface ArtistsResponse {
  artists: HomeArtist[];
  lastToken?: string;
}
