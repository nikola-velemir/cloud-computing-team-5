import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubscribeList } from './subscribe-list';

describe('SubscribeList', () => {
  let component: SubscribeList;
  let fixture: ComponentFixture<SubscribeList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubscribeList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubscribeList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
