import { AritstViewAlbumResponse } from './artist-view-album-response';
import { ArtistViewSongResponse } from './artist-view-song-response';

export interface ArtistViewResponse {
  id: string;
  name: string;
  biogaphy: string;
  songs: ArtistViewSongResponse[];
  albums: AritstViewAlbumResponse[];
}
