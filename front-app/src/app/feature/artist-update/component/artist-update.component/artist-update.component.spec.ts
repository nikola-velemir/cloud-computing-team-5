import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArtistUpdateComponent } from './artist-update.component';

describe('ArtistUpdateComponent', () => {
  let component: ArtistUpdateComponent;
  let fixture: ComponentFixture<ArtistUpdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ArtistUpdateComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ArtistUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
