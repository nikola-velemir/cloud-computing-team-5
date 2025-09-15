import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SongView } from './song-view';

describe('SongView', () => {
  let component: SongView;
  let fixture: ComponentFixture<SongView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SongView]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SongView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
