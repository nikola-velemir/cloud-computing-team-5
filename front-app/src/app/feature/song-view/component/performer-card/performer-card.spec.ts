import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PerformerCard } from './performer-card';

describe('PerformerCard', () => {
  let component: PerformerCard;
  let fixture: ComponentFixture<PerformerCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PerformerCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PerformerCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
