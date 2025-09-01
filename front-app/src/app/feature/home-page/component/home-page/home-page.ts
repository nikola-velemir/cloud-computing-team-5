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
  songsPrevTokens: string[] = [];
  songsNextToken?: string = '';
  songsPrevDisabled: boolean = true;
  songsLimit = 1;

  albums: HomeAlbum[] = [];
  albumPrevTokens: string[] = [];
  albumsNextToken?: string = '';
  albumPrevDisabled: boolean = true;
  albumsLimit = 4;

  artists: HomeArtist[] = [];
  artistsPrevTokens: string[] = [];
  artistsNextToken?: string = '';
  artistsPrevDisabled: boolean = true;
  artistsLimit = 4;

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
    this.songService
      .getSongs(this.songsLimit, this.songsNextToken)
      .subscribe((response) => {
        if (response.songs.length != 0) {
          this.songs = response.songs;
          if (this.songsNextToken) {
            this.songsPrevTokens.push(this.songsNextToken);
          }
        }
        this.songsNextToken = response.lastToken;
      });
  }

  getNextSongs() {
    if (this.songsNextToken && this.songs.length == this.songsLimit) {
      this.songsPrevDisabled = false;
      this.loadSongs();
    }
  }

  getPrevSongs() {
    this.songsPrevTokens.pop();
    this.songsNextToken = this.songsPrevTokens.pop();
    if (this.songsPrevTokens.length === 0) {
      this.songsPrevDisabled = true;
      this.songsPrevTokens.push('');
    }
    this.loadSongs();
  }

  loadArtists() {
    this.artistService
      .getArtists(this.artistsLimit, this.artistsNextToken)
      .subscribe((response) => {
        if (response.artists.length != 0) {
          this.artists = response.artists;
          if (this.artistsNextToken) {
            this.artistsPrevTokens.push(this.artistsNextToken);
          }
        }
        this.artistsNextToken = response.lastToken;
      });
  }

  getNextArtists() {
    if (this.artistsNextToken && this.artists.length == this.artistsLimit) {
      this.artistsPrevDisabled = false;
      this.loadArtists();
    }
  }

  getPrevArtists() {
    this.artistsPrevTokens.pop();
    this.artistsNextToken = this.artistsPrevTokens.pop();
    if (this.artistsPrevTokens.length === 0) {
      this.artistsPrevDisabled = true;
      this.artistsPrevTokens.push('');
    }
    this.loadArtists();
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
