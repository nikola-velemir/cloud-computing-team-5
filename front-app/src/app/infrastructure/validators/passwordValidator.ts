import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function passwordValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;
    //Ab1!xY2@

    const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]).+$/


    if (!value) {
      return null;
    }

    const isValid = passwordPattern.test(value);

    return isValid ? null : { invalidPassword: true };
  };
}
