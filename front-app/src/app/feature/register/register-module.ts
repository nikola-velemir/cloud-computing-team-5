import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { RegisterForm } from './component/register-form/register-form';
import {RouterLink} from '@angular/router';

@NgModule({
  declarations: [RegisterForm],
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
})
export class RegisterModule {}
