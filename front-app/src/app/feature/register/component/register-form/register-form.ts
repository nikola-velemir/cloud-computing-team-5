import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { passwordValidator } from '../../../../infrastructure/validators/passwordValidator';
import { matchPasswords } from '../../../../infrastructure/validators/matchPasswords.validator';
import { RegisterService } from '../../service/register.service';
import { RegisterRequest } from '../../model/register.request';

@Component({
  selector: 'app-register-form',
  standalone: false,
  templateUrl: './register-form.html',
  styleUrl: './register-form.scss',
})
export class RegisterForm implements OnInit {
  form!: FormGroup;
  showPassword = false;
  showConfirmPassword = false;
  waitingResponse = false;

  constructor(
    private fb: FormBuilder,
    private dialog: MatDialog,
    private registerService: RegisterService
  ) {}

  ngOnInit(): void {
    this.form = this.fb.group(
      {
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, passwordValidator()]],
        confirmPassword: ['', Validators.required],
        firstName: ['', Validators.required],
        lastName: ['', Validators.required],
        username: ['', Validators.required],
        dateOfBirth: ['', Validators.required],
      },
      { validators: matchPasswords('password', 'confirmPassword') }
    );
  }

  get email() {
    return this.form.get('email');
  }

  get password() {
    return this.form.get('password');
  }

  get confirmPassword() {
    return this.form.get('confirmPassword');
  }

  get firstName() {
    return this.form.get('firstName');
  }

  get lastName() {
    return this.form.get('lastName');
  }

  get username() {
    return this.form.get('username');
  }

  get dateOfBirth() {
    return this.form.get('dateOfBirth');
  }

  togglePasswordVisibility(field: 'password' | 'confirmPassword') {
    if (field === 'password') {
      this.showPassword = !this.showPassword;
    } else {
      this.showConfirmPassword = !this.showConfirmPassword;
    }
  }

  async onSubmit() {
    if (this.form.valid) {
      this.waitingResponse = true;
      const formValues = this.form.value;
      const registerRequest: RegisterRequest = {
        firstName: formValues.firstName,
        lastName: formValues.lastName,
        dateOfBirth: formValues.dateOfBirth,
        username: formValues.username,
        email: formValues.email,
        password: formValues.password,
      };
      this.registerService.register(registerRequest);
    }
  }
}
