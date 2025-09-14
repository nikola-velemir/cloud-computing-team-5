import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeArtistCard } from './home-artist-card';

describe('HomeArtistCard', () => {
  let component: HomeArtistCard;
  let fixture: ComponentFixture<HomeArtistCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeArtistCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeArtistCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
