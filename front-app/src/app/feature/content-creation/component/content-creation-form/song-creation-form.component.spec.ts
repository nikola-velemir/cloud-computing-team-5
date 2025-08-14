import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SongCreationForm } from './song-creation-form.component';

describe('ContentCreationForm', () => {
  let component: SongCreationForm;
  let fixture: ComponentFixture<SongCreationForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SongCreationForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SongCreationForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
