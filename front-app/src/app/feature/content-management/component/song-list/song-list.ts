import { Component, OnInit } from '@angular/core';
import { Song } from '../../model/song.model';
import { ContentManagementService } from '../../service/content-management.service';
import { ToastService } from '../../../../shared/toast/service/toast-service';
import { Router } from '@angular/router';
import { SongsResponse } from '../../model/song.response';

@Component({
  selector: 'app-song-list',
  standalone: false,
  templateUrl: './song-list.html',
  styleUrl: './song-list.scss',
})
export class SongList implements OnInit {
  currentPage: number = 0;
  songs: Song[] = [];
  showCreate = false;
  pageSize: number = 8;
  prevTokens: string[] = [];
  nextToken?: string = '';
  prevDisabled: boolean = true;
  loading: boolean = false;
  showConfirmDelete = false;
  songToDelete: string | null = null;

  constructor(
    private contentManagementService: ContentManagementService,
    private toast: ToastService,
    private router: Router
  ) {}

  toggleCreate() {
    this.router.navigate(['/content-creation']);
  }

  ngOnInit(): void {
    this.loadAlbums();
  }

  loadAlbums() {
    this.contentManagementService
      .loadSongs(this.pageSize, this.nextToken)
      .subscribe((response: SongsResponse) => {
        if (response.songs.length != 0) {
          this.songs = response.songs;
          if (this.nextToken) {
            this.prevTokens.push(this.nextToken);
          }
        } else {
          this.songs = [];
          this.nextToken = '';
        }
        this.nextToken = response.lastToken;
      });
  }
  loadNext() {
    if (this.nextToken && this.songs.length == this.pageSize) {
      this.prevDisabled = false;
      this.loadAlbums();
    }
  }
  loadPrev() {
    this.prevTokens.pop();
    this.nextToken = this.prevTokens.pop();
    if (this.prevTokens.length === 0) {
      this.prevDisabled = true;
      this.prevTokens.push('');
    }
    this.loadAlbums();
  }

  deleteAlbum(id: string) {
    this.loading = true;
    this.contentManagementService.deleteAlbum(id).subscribe({
      next: (response: boolean) => {
        this.loading = false;
        console.log(response);
        if (response) {
          this.toast.success('You delete artist');
          this.loadAlbums();
        }
      },
      error: (err) => {
        this.loading = false;
        console.log(err);
        this.toast.error('Error');
      },
    });
  }

  openConfirmDelete(id: string) {
    this.songToDelete = id;
    this.showConfirmDelete = true;
  }

  handleConfirm(result: boolean) {
    this.showConfirmDelete = false;
    if (result && this.songToDelete) {
      this.deleteAlbum(this.songToDelete);
    }
    this.songToDelete = null;
  }
}
