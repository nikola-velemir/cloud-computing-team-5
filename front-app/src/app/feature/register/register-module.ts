import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { RegisterForm } from './component/register-form/register-form';

@NgModule({
  declarations: [RegisterForm],
  imports: [CommonModule, ReactiveFormsModule],
})
export class RegisterModule {}
