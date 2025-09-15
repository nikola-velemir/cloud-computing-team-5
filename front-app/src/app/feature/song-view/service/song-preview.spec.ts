import { TestBed } from '@angular/core/testing';

import { SongPreviewService } from './song-preview';

describe('SongPreview', () => {
  let service: SongPreviewService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SongPreviewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
