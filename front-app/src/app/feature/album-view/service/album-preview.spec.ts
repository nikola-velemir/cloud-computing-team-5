import { TestBed } from '@angular/core/testing';

import { AlbumPreviewService } from './album-preview';

describe('AlbumPreview', () => {
  let service: AlbumPreviewService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AlbumPreviewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
