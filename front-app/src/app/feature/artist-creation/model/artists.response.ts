import { ArtistDTO } from './artistDTO.response';

export interface ArtistsResponse {
  artists: ArtistDTO[];
  lastToken: string;
}
