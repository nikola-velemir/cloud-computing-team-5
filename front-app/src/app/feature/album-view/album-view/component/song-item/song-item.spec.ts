import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SongItem } from './song-item';

describe('SongItem', () => {
  let component: SongItem;
  let fixture: ComponentFixture<SongItem>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SongItem]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SongItem);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
