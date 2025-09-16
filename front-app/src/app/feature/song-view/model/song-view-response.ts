import { SongViewAlbumResponse } from './song-view-album-response';
import { SongViewArtistResponse } from './song-view-artist-response';

export interface SongViewResponse {
  id: string;
  name: string;
  artists: SongViewArtistResponse[];
  album: SongViewAlbumResponse;
  imageUrl: string;
  lyrics: string | null;
}
