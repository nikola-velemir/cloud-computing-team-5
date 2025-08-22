import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewAlbumForm } from './new-album-form';

describe('NewAlbumForm', () => {
  let component: NewAlbumForm;
  let fixture: ComponentFixture<NewAlbumForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewAlbumForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewAlbumForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
