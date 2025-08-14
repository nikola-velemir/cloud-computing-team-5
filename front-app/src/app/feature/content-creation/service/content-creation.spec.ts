import { TestBed } from '@angular/core/testing';

import { ContentCreationService } from './content-creation.service';

describe('ContentCreation', () => {
  let service: ContentCreationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ContentCreationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
