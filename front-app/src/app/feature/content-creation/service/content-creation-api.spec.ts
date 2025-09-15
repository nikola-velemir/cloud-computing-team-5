import { TestBed } from '@angular/core/testing';

import { ContentCreationApi } from './content-creation-api';

describe('ContentCreationApi', () => {
  let service: ContentCreationApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ContentCreationApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
