import {AbstractControl, ValidationErrors} from '@angular/forms';

export const fileTypeValidator = (allowedTypes: string[]) => {
  return (control: AbstractControl): ValidationErrors | null => {
    const files: FileList = control.value;
    if (!files) {
      return null;
    }
    for (let file of files) {

      const extension = file.name.split('.').pop()?.toLowerCase();
      if (!extension || !allowedTypes.includes(extension)) {
        return {fileType: true};
      }
    }
    return null;
  }
}
