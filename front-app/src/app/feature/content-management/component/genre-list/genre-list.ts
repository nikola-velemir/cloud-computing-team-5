import { Component, OnInit } from '@angular/core';
import { ToastService } from '../../../../shared/toast/service/toast-service';
import { AlbumsResponse } from '../../model/albums.response';
import { ContentManagementService } from '../../service/content-management.service';
import { Genre } from '../../model/genre.model';
import { Router } from '@angular/router';
import { GenresResponse } from '../../model/genres.response';

@Component({
  selector: 'app-genre-list',
  standalone: false,
  templateUrl: './genre-list.html',
  styleUrl: './genre-list.scss',
})
export class GenreList implements OnInit {
  currentPage: number = 0;
  genres: Genre[] = [];
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
    this.router.navigate(['/genre-creation']);
  }

  ngOnInit(): void {
    this.loadGenres();
  }

  loadGenres() {
    this.contentManagementService
      .loadGenres(this.pageSize, this.nextToken)
      .subscribe((response: GenresResponse) => {
        if (response.genres.length != 0) {
          this.genres = response.genres;
          if (this.nextToken) {
            this.prevTokens.push(this.nextToken);
          }
        } else {
          this.genres = [];
          this.nextToken = '';
        }
        this.nextToken = response.lastToken;
      });
  }
  loadNext() {
    if (this.nextToken && this.genres.length == this.pageSize) {
      this.prevDisabled = false;
      this.loadGenres();
    }
  }
  loadPrev() {
    this.prevTokens.pop();
    this.nextToken = this.prevTokens.pop();
    if (this.prevTokens.length === 0) {
      this.prevDisabled = true;
      this.prevTokens.push('');
    }
    this.loadGenres();
  }

  deleteAlbum(id: string) {
    this.loading = true;
    this.contentManagementService.deleteAlbum(id).subscribe({
      next: (response: boolean) => {
        this.loading = false;
        console.log(response);
        if (response) {
          this.toast.success('You delete artist');
          this.loadGenres();
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
