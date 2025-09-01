import { Component, OnInit } from '@angular/core';
import { FeedService } from '../../service/feed.service';
import { FeedCardData } from '../../model/feed-card.model';
import { HomeAlbum } from '../../model/home-album.model';
import { HomeSong } from '../../model/home-song.mode';
import { HomeArtist } from '../../model/home-artist.model';
import { AlbumService } from '../../service/album.service';
import { ArtistService } from '../../service/artist.service';
import { SongService } from '../../service/song.service';

@Component({
  selector: 'app-home-page',
  standalone: false,
  templateUrl: './home-page.html',
  styleUrl: './home-page.scss',
})
export class HomePage implements OnInit {
  currentPage = 1;
  pageSize = 5;
  totalPages = 0;
  feeds: FeedCardData[] = [];
  songs: HomeSong[] = [];
  albums: HomeAlbum[] = [];
  albumPrevTokens: string[] = [];
  albumsNextToken?: string = '';
  albumPrevDisabled: boolean = true;
  albumsLimit = 1;
  artists: HomeArtist[] = [];

  constructor(
    private feedService: FeedService,
    private albumService: AlbumService,
    private artistService: ArtistService,
    private songService: SongService
  ) {}

  ngOnInit() {
    this.loadFeed();
    this.loadSongs();
    this.loadAlbums();
    this.loadArtists();
    this.albumPrevTokens.push('');
  }

  loadFeed() {
    this.feedService.getFeed().subscribe((feeds) => {
      this.feeds = feeds;
    });
  }

  loadSongs() {
    this.songService.getSongs().subscribe((songs) => {
      this.songs = songs;
    });
  }

  loadArtists() {
    this.artistService.getArtists().subscribe((artists) => {
      this.artists = artists;
    });
  }

  loadAlbums() {
    this.albumService
      .getAlbums(this.albumsLimit, this.albumsNextToken)
      .subscribe((response) => {
        if (response.albums.length != 0) {
          this.albums = response.albums;
          if (this.albumsNextToken) {
            this.albumPrevTokens.push(this.albumsNextToken);
          }
        }
        this.albumsNextToken = response.lastToken;
      });
  }

  getNextAlbums() {
    if (this.albumsNextToken && this.albums.length == this.albumsLimit) {
      this.albumPrevDisabled = false;
      this.loadAlbums();
    }
  }

  getPrevAlbums() {
    this.albumPrevTokens.pop();
    this.albumsNextToken = this.albumPrevTokens.pop();
    if (this.albumPrevTokens.length === 0) {
      this.albumPrevDisabled = true;
      this.albumPrevTokens.push('');
    }
    this.loadAlbums();
  }

  nextSongPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.loadSongs();
    }
  }

  prevSongPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadSongs();
    }
  }
}
