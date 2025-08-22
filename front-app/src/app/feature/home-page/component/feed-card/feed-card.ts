import { Component, Input } from '@angular/core';
import { FeedCardData } from '../../model/feed-card.model';
import { FeedType } from '../../model/feed-type.mode';
import { Router } from '@angular/router';

@Component({
  selector: 'app-feed-card',
  standalone: false,
  templateUrl: './feed-card.html',
  styleUrl: './feed-card.scss',
})
export class FeedCard {
  @Input()
  feed!: FeedCardData;

  constructor(private router: Router) {}

  open() {
    if (this.feed.type == FeedType.Album) {
      this.router.navigate([`/album/${this.feed.id}`]);
    } else {
      this.router.navigate([`/song/${this.feed.id}`]);
    }
  }
}
