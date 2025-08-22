import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Navbar } from './component/navbar/navbar';
import { AuthModule } from '../../infrastructure/auth/auth-module';

@NgModule({
  declarations: [Navbar],
  imports: [CommonModule, RouterModule, AuthModule],
  exports: [Navbar],
})
export class NavModule {}
