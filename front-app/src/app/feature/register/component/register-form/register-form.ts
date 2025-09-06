import { Component, OnInit } from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { passwordValidator } from '../../../../infrastructure/validators/passwordValidator';
import { matchPasswords } from '../../../../infrastructure/validators/matchPasswords.validator';
import { RegisterService } from '../../service/register.service';
import { RegisterRequest } from '../../model/register.request';
import {Router} from '@angular/router';

@Component({
  selector: 'app-register-form',
  standalone: false,
  templateUrl: './register-form.html',
  styleUrl: './register-form.scss',
})
export class RegisterForm implements OnInit {
  form: FormGroup;
  waitingResponse = false;
  errorMessage: string | null = null;
  showPassword = false;
  showConfirmPassword = false;

  constructor(
    private fb: FormBuilder,
    private dialog: MatDialog,
    private registerService: RegisterService,
    private router:Router,
  ) {
    this.form = this.fb.group({
      firstName: ['', [Validators.required]],
      lastName: ['', [Validators.required]],
      username: ['', [Validators.required]],
      dateOfBirth: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8), passwordValidator()]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordsMatchValidator });
  }

  ngOnInit(): void {

  }
  get firstName() { return this.form.get('firstName'); }
  get lastName() { return this.form.get('lastName'); }
  get username() { return this.form.get('username'); }
  get dateOfBirth() { return this.form.get('dateOfBirth'); }
  get email() { return this.form.get('email'); }
  get password() { return this.form.get('password'); }
  get confirmPassword() { return this.form.get('confirmPassword'); }

  togglePasswordVisibility(field: 'password' | 'confirmPassword') {
    if (field === 'password') this.showPassword = !this.showPassword;
    if (field === 'confirmPassword') this.showConfirmPassword = !this.showConfirmPassword;
  }

  passwordsMatchValidator(group: AbstractControl) {
    const password = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    if (password !== confirm) {
      group.get('confirmPassword')?.setErrors({ passwordMismatch: true });
    } else {
      group.get('confirmPassword')?.setErrors(null);
    }
    return null;
  }

  getRegisterRequest(): RegisterRequest {
    const formValue = this.form.value;

    return {
      name: formValue.firstName,
      lastname: formValue.lastName,
      birthday: new Date(formValue.dateOfBirth).toISOString().slice(0, 10),
      username: formValue.username,
      email: formValue.email,
      password: formValue.password
    };
  }
  onSubmit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.waitingResponse = true;
    this.errorMessage = null;

    const registerRequest = this.getRegisterRequest();
    console.log(registerRequest);
    this.registerService.register(registerRequest).subscribe({
      next: (res) => {
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.log(err);
        this.errorMessage = err || 'Registration failed';
        this.waitingResponse = false;
      },
      complete: () => this.waitingResponse = false
    });
  }
}
