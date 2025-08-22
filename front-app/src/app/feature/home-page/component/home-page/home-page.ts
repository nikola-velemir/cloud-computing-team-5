import { Component, OnInit } from '@angular/core';
import { SongData } from '../../../content-creation/service/content-creation.service';
import { FeedService } from '../../service/feed.service';
import { FeedCardData } from '../../model/feed-card.model';

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
  songs: SongData[] = [];
  feeds: FeedCardData[] = [];

  constructor(private feedService: FeedService) {}

  ngOnInit() {
    this.loadSongs();
    this.loadFeed();
  }
  loadFeed() {
    this.feedService.getFeed().subscribe((feeds) => {
      this.feeds = feeds;
    });
  }

  loadSongs() {
    // this.songService.getSongs(this.currentPage, this.pageSize).subscribe((res) => {
    //   this.songs = res.items;
    //   this.totalPages = res.totalPages; // Backend treba da šalje total
    // });
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
