import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../../service/login.service';

@Component({
  selector: 'app-login-form',
  standalone: false,
  templateUrl: './login-form.html',
  styleUrl: './login-form.scss',
})
export class LoginForm implements OnInit {
  form!: FormGroup;
  showPassword: boolean = false;
  waitingResponse = false;
  redirectUrl!: string;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
    });
  }

  get email() {
    return this.form.get('email');
  }

  get password() {
    return this.form.get('password');
  }

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  async onSubmit() {}
}
