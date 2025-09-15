import { TestBed } from '@angular/core/testing';

import { AudioApi } from './audio-api.service';

describe('AudioService', () => {
  let service: AudioApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AudioApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
