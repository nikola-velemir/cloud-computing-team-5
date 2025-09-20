import { Component, OnInit } from '@angular/core';
import { ArtistForm } from '../artist-form/artist-form';
import { CommonModule, NgIf } from '@angular/common';
import { ArtistDTO } from '../../model/artistDTO.response';
import { ArtistService } from '../../service/artist-service';
import { ArtistsResponse } from '../../model/artists.response';
import { ToastService } from '../../../../shared/toast/service/toast-service';
import { ConfirmDialog } from '../../../../shared/component/confirm-dialog/confirm-dialog';

@Component({
  selector: 'app-artist-list',
  imports: [ArtistForm, NgIf, CommonModule, ConfirmDialog],
  templateUrl: './artist-list.html',
  styleUrl: './artist-list.scss',
})
export class ArtistList implements OnInit {
  currentPage: number = 0;
  artists: ArtistDTO[] = [];
  showCreate = false;
  pageSize: number = 8;
  prevTokens: string[] = [];
  nextToken?: string = '';
  prevDisabled: boolean = true;
  loading: boolean = false;
  showConfirmDelete = false;
  artistToDelete: string | null = null;

  constructor(
    private artistService: ArtistService,
    private toast: ToastService
  ) {}

  toggleCreate() {
    this.showCreate = !this.showCreate;
    this.loadArtists();
  }

  ngOnInit(): void {
    this.loadArtists();
  }

  loadArtists() {
    this.artistService
      .loadArtists(this.pageSize, this.nextToken)
      .subscribe((response: ArtistsResponse) => {
        if (response.artists.length != 0) {
          this.artists = response.artists;
          if (this.nextToken) {
            this.prevTokens.push(this.nextToken);
          }
        } else {
          this.artists = [];
          this.nextToken = '';
        }
        this.nextToken = response.lastToken;
      });
  }

  loadNext() {
    if (this.nextToken && this.artists.length == this.pageSize) {
      this.prevDisabled = false;
      this.loadArtists();
    }
  }
  loadPrev() {
    this.prevTokens.pop();
    this.nextToken = this.prevTokens.pop();
    if (this.prevTokens.length === 0) {
      this.prevDisabled = true;
      this.prevTokens.push('');
    }
    this.loadArtists();
  }

  deleteArtist(id: string) {
    this.loading = true;
    this.artistService.deleteArtist(id).subscribe({
      next: (response: boolean) => {
        this.loading = false;
        console.log(response);
        if (response) {
          this.toast.success('You deleted artist');
          this.loadArtists();
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
    this.artistToDelete = id;
    this.showConfirmDelete = true;
  }

  handleConfirm(result: boolean) {
    this.showConfirmDelete = false;
    if (result && this.artistToDelete) {
      this.deleteArtist(this.artistToDelete);
    }
    this.artistToDelete = null;
  }
}
