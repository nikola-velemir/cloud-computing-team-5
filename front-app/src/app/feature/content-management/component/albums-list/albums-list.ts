import { Component, OnInit } from '@angular/core';
import { ToastService } from '../../../../shared/toast/service/toast-service';
import { ContentManagementService } from '../../service/content-management.service';
import { AlbumsResponse } from '../../model/albums.response';
import { Album } from '../../model/album.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-albums-list',
  standalone: false,
  templateUrl: './albums-list.html',
  styleUrl: './albums-list.scss',
})
export class AlbumsList implements OnInit {
  currentPage: number = 0;
  albums: Album[] = [];
  showCreate = false;
  pageSize: number = 8;
  prevTokens: string[] = [];
  nextToken?: string = '';
  prevDisabled: boolean = true;
  loading: boolean = false;
  showConfirmDelete = false;
  albumToDelete: string | null = null;

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
      .loadAlbums(this.pageSize, this.nextToken)
      .subscribe((response: AlbumsResponse) => {
        if (response.albums.length != 0) {
          this.albums = response.albums;
          if (this.nextToken) {
            this.prevTokens.push(this.nextToken);
          }
        } else {
          this.albums = [];
          this.nextToken = '';
        }
        this.nextToken = response.lastToken;
      });
  }
  loadNext() {
    if (this.nextToken && this.albums.length == this.pageSize) {
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
          this.toast.success('You deleted album');
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
    this.albumToDelete = id;
    this.showConfirmDelete = true;
  }

  handleConfirm(result: boolean) {
    this.showConfirmDelete = false;
    if (result && this.albumToDelete) {
      this.deleteAlbum(this.albumToDelete);
    }
    this.albumToDelete = null;
  }
}
