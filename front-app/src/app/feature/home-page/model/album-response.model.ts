import { HomeAlbum } from './home-album.model';

export interface AlbumsResponse {
  albums: HomeAlbum[];
  lastToken?: string;
}
