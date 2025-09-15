import { TestBed } from '@angular/core/testing';

import { DiscoverPageService } from './discover-page.service';

describe('DiscoverPageService', () => {
  let service: DiscoverPageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DiscoverPageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
