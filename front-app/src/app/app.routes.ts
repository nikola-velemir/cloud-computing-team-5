import { Routes } from '@angular/router';
import { ContentCreationForm } from './feature/content-creation/component/content-creation-form/content-creation-form.component';
import { SongView } from './feature/song-view/component/song-view/song-view';
import { AlbumView } from './feature/album-view/album-view/component/album-view/album-view';
import { PerformerView } from './feature/performer-view/component/performer-view/performer-view';
import { LoginForm } from './feature/login/component/login-form/login-form';
import { GenreView } from './feature/genre-view/component/genre-view/genre-view';
import { RegisterForm } from './feature/register/component/register-form/register-form';
import { GenreCreationForm } from './feature/category-creation/genre-creation-form/genre-creation-form';
import { HomePage } from './feature/home-page/component/home-page/home-page';
import { DiscoverPage } from './feature/home-page/component/discover-page/discover-page';
import {AuthGuard} from './infrastructure/auth-guard/auth.guard';

export const routes: Routes = [
  { path: '', component: HomePage, canActivate: [AuthGuard], data: {roles: ['Admin', 'AuthenticatedUser']} },

  { path: 'login', component: LoginForm },
  { path: 'register', component: RegisterForm },

  { path: 'discover', component: DiscoverPage, canActivate: [AuthGuard] },
  { path: 'manage-content', component: DiscoverPage, canActivate: [AuthGuard] },
  { path: 'content-creation', component: ContentCreationForm, canActivate: [AuthGuard] },
  { path: 'song/:id', component: SongView, canActivate: [AuthGuard] },
  { path: 'album/:id', component: AlbumView, canActivate: [AuthGuard] },
  { path: 'performer/:id', component: PerformerView, canActivate: [AuthGuard] },
  { path: 'genre/:id', component: GenreView, canActivate: [AuthGuard] },
  { path: 'genre-creation', component: GenreCreationForm, canActivate: [AuthGuard] },

  { path: '**', redirectTo: 'login' }
];
