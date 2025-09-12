import { Component, OnInit } from '@angular/core';
import { Genre } from '../../model/genre.model';
import { GenresResponse } from '../../model/genres-response.model';
import { DiscoverPageService } from '../../service/discover-page.service';
import { Artist } from '../../model/artist.model';
import { Album } from '../../model/album.model';
import { AlbumsResponse } from '../../model/albums-response.model';
import { ArtistsResponse } from '../../model/artists-response';
import { Song } from '../../model/song.model';

@Component({
  selector: 'app-discover-page',
  standalone: false,
  templateUrl: './discover-page.html',
  styleUrl: './discover-page.scss',
})
export class DiscoverPage implements OnInit {
  genres: Genre[] = [];
  selectedGenreId: string = '';

  selectedType: 'artists' | 'albums' = 'artists';

  artists: Artist[] = [];
  selectedArtist?: Artist;
  artistsEnabled: boolean = false;

  albums: Album[] = [];
  selectedAlbum?: Album;
  albumsEnabled: boolean = true;

  songs: Song[] = [];
  songTotapPages = 1;
  songPageSize = 10;
  songCurrentPage = 0;

  constructor(private service: DiscoverPageService) {}

  ngOnInit(): void {
    this.getGenres();
  }

  onTypeChange() {
    this.fetchOptions();
  }

  getGenres() {
    this.service.getGenres().subscribe({
      next: (response: GenresResponse) => {
        this.genres = response.genres;
      },
    });
  }

  fetchOptions() {
    if (this.selectedGenreId) {
      if (this.selectedType == 'artists') {
        this.service.getArtists(this.selectedGenreId).subscribe({
          next: (response: ArtistsResponse) => {
            this.artists = response.artists;
            this.selectedArtist = undefined;
          },
        });
      } else {
        this.service.getAlbums(this.selectedGenreId).subscribe({
          next: (response: AlbumsResponse) => {
            this.albums = response.albums;
            this.selectedAlbum = undefined;
          },
        });
      }
    }
  }

  getNextSongs() {
    throw new Error('Method not implemented.');
  }
  getPrevSongs() {
    throw new Error('Method not implemented.');
  }
}
