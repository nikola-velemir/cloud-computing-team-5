import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PerformerAlbumStep } from './performer-album-step';

describe('PerformerAlbumStep', () => {
  let component: PerformerAlbumStep;
  let fixture: ComponentFixture<PerformerAlbumStep>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PerformerAlbumStep]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PerformerAlbumStep);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
