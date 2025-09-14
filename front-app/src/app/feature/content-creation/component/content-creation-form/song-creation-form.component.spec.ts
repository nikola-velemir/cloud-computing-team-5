import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentCreationForm } from './content-creation-form.component';

describe('ContentCreationForm', () => {
  let component: ContentCreationForm;
  let fixture: ComponentFixture<ContentCreationForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContentCreationForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentCreationForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
