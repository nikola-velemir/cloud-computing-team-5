import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MetadataForm } from './metadata-form';

describe('MetadataForm', () => {
  let component: MetadataForm;
  let fixture: ComponentFixture<MetadataForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MetadataForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MetadataForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
