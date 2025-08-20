import { Routes } from '@angular/router';
import { ContentCreationForm } from './feature/content-creation/component/content-creation-form/content-creation-form.component';
import { SongView } from './feature/song-view/component/song-view/song-view';
import { AlbumView } from './feature/album-view/album-view/component/album-view/album-view';
import { PerformerView } from './feature/performer-view/component/performer-view/performer-view';
import { LoginForm } from './feature/login/component/login-form/login-form';
import { RegisterForm } from './feature/register/component/register-form/register-form';

export const routes: Routes = [
  { path: 'content-creation', component: ContentCreationForm },
  { path: 'song/:id', component: SongView },
  { path: 'album/:id', component: AlbumView },
  { path: 'performer/:id', component: PerformerView },
  { path: 'login', component: LoginForm },
  { path: 'register', component: RegisterForm },
];
