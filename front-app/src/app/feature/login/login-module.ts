import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginForm } from './component/login-form/login-form';
import { ReactiveFormsModule } from '@angular/forms';
import {RouterLink} from "@angular/router";

@NgModule({
    declarations: [LoginForm],
    imports: [CommonModule, ReactiveFormsModule, RouterLink],
    exports: [
        LoginForm
    ]
})
export class LoginModule {}
