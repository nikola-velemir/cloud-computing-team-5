import { Component, OnInit } from '@angular/core';
import { Genre } from '../../model/genre.model';
import { GenresResponse } from '../../model/genres-response.model';
import { DiscoverPageService } from '../../service/discover-page.service';

@Component({
  selector: 'app-discover-page',
  standalone: false,
  templateUrl: './discover-page.html',
  styleUrl: './discover-page.scss',
})
export class DiscoverPage implements OnInit {
  genres: Genre[] = [];
  selectedGenre!: Genre;

  constructor(private service: DiscoverPageService) {}

  ngOnInit(): void {
    this.getGenres();
  }

  getGenres() {
    this.service.getGenres().subscribe({
      next: (response: GenresResponse) => {
        this.genres = response.genres;
      },
    });
  }

  onGenreChange($event: Event) {
    throw new Error('Method not implemented.');
  }
}
