import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArtistStep } from './artist-step';

describe('PerformerAlbumStep', () => {
  let component: ArtistStep;
  let fixture: ComponentFixture<ArtistStep>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ArtistStep],
    }).compileComponents();

    fixture = TestBed.createComponent(ArtistStep);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
