import { TestBed } from '@angular/core/testing';

import { PerformerViewService } from './performer-view-service';

describe('PerformerViewService', () => {
  let service: PerformerViewService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PerformerViewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
