import { AlbumViewArtistResponse } from './album-view-artist-response';
import { AlbumViewSongResponse } from './album-view-song-response';

export interface AlbumViewResponse {
  id: string;
  imageUrl: string;
  title: string;
  releaseDate: string;
  artists: AlbumViewArtistResponse[];
  songs: AlbumViewSongResponse[];
}
