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

export const routes: Routes = [
  { path: '', component: HomePage },
  { path: 'discover', component: DiscoverPage },
  { path: 'manage-content', component: DiscoverPage },
  { path: 'content-creation', component: ContentCreationForm },
  { path: 'song/:id', component: SongView },
  { path: 'album/:id', component: AlbumView },
  { path: 'performer/:id', component: PerformerView },
  { path: 'login', component: LoginForm },
  { path: 'genre/:id', component: GenreView },
  { path: 'register', component: RegisterForm },
  { path: 'genre-creation', component: GenreCreationForm },
];
