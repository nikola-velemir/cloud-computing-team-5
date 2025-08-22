import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileUploadStep } from './file-upload-step';

describe('FileUploadStep', () => {
  let component: FileUploadStep;
  let fixture: ComponentFixture<FileUploadStep>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FileUploadStep]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FileUploadStep);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
