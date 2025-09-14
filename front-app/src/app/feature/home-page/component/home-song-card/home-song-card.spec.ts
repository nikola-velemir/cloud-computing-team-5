import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeSongCard } from './home-song-card';

describe('HomeSongCard', () => {
  let component: HomeSongCard;
  let fixture: ComponentFixture<HomeSongCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeSongCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeSongCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
