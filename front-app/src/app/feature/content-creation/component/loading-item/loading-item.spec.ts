import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadingItem } from './loading-item';

describe('LoadingItem', () => {
  let component: LoadingItem;
  let fixture: ComponentFixture<LoadingItem>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoadingItem]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoadingItem);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
