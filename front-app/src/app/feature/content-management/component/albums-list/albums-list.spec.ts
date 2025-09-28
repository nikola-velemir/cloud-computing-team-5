import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlbumsList } from './albums-list';

describe('AlbumsList', () => {
  let component: AlbumsList;
  let fixture: ComponentFixture<AlbumsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AlbumsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlbumsList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
