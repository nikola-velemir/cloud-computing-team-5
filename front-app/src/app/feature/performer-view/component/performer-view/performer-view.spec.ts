import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PerformerView } from './performer-view';

describe('PerformerView', () => {
  let component: PerformerView;
  let fixture: ComponentFixture<PerformerView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PerformerView]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PerformerView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
