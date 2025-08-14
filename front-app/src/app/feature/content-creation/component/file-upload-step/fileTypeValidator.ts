import {AbstractControl, ValidationErrors} from '@angular/forms';

export const fileTypeValidator = (allowedTypes: string[]) => {
  return (control: AbstractControl): ValidationErrors | null => {
    const file: File = control.value;
    console.log(file)
    if (!file) {
      return null;
    }
    const extension = file.name.split('.').pop()?.toLowerCase();
    if (!extension || !allowedTypes.includes(extension)) {
      return {fileType: true};
    }
    console.log("HERE")
    return null;
  }
}
