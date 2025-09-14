import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlbumView } from './album-view';

describe('AlbumView', () => {
  let component: AlbumView;
  let fixture: ComponentFixture<AlbumView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AlbumView]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlbumView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
