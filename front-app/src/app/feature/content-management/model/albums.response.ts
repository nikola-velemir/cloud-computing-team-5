import { Album } from './album.model';

export interface AlbumsResponse {
  albums: Album[];
  lastToken?: string;
}
