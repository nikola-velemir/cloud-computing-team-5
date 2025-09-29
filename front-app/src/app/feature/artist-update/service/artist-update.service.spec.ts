import { TestBed } from '@angular/core/testing';

import { ArtistUpdateService } from './artist-update.service';

describe('ArtistUpdateService', () => {
  let service: ArtistUpdateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ArtistUpdateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
