import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SongListItem } from './song-list-item';

describe('SongListItem', () => {
  let component: SongListItem;
  let fixture: ComponentFixture<SongListItem>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SongListItem]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SongListItem);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
