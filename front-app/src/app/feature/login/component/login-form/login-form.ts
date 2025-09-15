import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../../service/login.service';
import { Router } from '@angular/router';

import {firstValueFrom, switchMap, take, tap} from 'rxjs';
import {ToastService} from '../../../../shared/toast/service/toast-service';
import {passwordValidator} from '../../../../infrastructure/validators/passwordValidator';



@Component({
  selector: 'app-login-form',
  standalone: false,
  templateUrl: './login-form.html',
  styleUrl: './login-form.scss',
})
export class LoginForm implements OnInit {
  form: FormGroup;
  waitingResponse = false;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private loginService: LoginService,
    private router: Router,
    private toast:ToastService
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],

      password: ['', [Validators.required, passwordValidator()]]

    });
  }

  ngOnInit(): void {}

  get email() {
    return this.form.get('email');
  }

  get password() {
    return this.form.get('password');
  }

  async onSubmit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.waitingResponse = true;
    this.errorMessage = null;

    this.loginService.login(this.email?.value, this.password?.value).subscribe({
      next: (res) => {
        this.toast.success('Login successful');
        this.router.navigate(['/']);
      },
      error: (err) => {
        if (err.name !== 'AbortError') {
          this.errorMessage = 'Invalid email or password';
        }
        this.waitingResponse = false;
      },
      complete: () => {
        this.waitingResponse = false;
      },
    });
  }
}
