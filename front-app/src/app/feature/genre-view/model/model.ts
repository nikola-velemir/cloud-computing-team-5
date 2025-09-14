export interface GenreArtistPreviewResponse {
  id: string;
  name: string;
  imageUrl: string;
}

export interface GenreAlbumPreviewResponse {
  id: string;
  title: string;
  imageUrl: string;
  performerNames: string[];
  year: string;
}

export interface GenreSongPreviewResponse {
  id: string;
  name: string;
  imageUrl: string;
}

export interface GenrePreviewResponse {
  id: string;
  name: string;
  imageUrl: string;
  description: string;
  artists: GenreArtistPreviewResponse[];
  albums: GenreAlbumPreviewResponse[];
  songs: GenreSongPreviewResponse[];
}
