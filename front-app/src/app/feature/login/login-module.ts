import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginForm } from './component/login-form/login-form';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
    declarations: [LoginForm],
    imports: [CommonModule, ReactiveFormsModule],
    exports: [
        LoginForm
    ]
})
export class LoginModule {}
