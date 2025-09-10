import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeGenreCard } from './home-genre-card';

describe('HomeGenreCard', () => {
  let component: HomeGenreCard;
  let fixture: ComponentFixture<HomeGenreCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeGenreCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeGenreCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
