import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeAlbumCard } from './home-album-card';

describe('HomeAlbumCard', () => {
  let component: HomeAlbumCard;
  let fixture: ComponentFixture<HomeAlbumCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeAlbumCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeAlbumCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
