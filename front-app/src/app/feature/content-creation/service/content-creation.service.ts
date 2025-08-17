import {Injectable} from '@angular/core';
import {BehaviorSubject, Subject} from 'rxjs';
import {Genre} from '../model/genre';
import {Author} from '../model/author';
import {AlbumCreation} from '../model/albumCreation';

export interface SongData {
  id: number;
  songAudio: File | null | undefined;
  songImage: File | null | undefined;
  songName: string | null | undefined;
  songGenre: Genre | null | undefined;
  songAuthor: Author | null | undefined;
}

@Injectable({
  providedIn: 'root'
})
export class ContentCreationService {

  private currentStep = new BehaviorSubject(0);
  private currentSong = new BehaviorSubject<SongData | null>(null);
  private songs = new BehaviorSubject<SongData[]>([]);
  private createdAlbum = new BehaviorSubject<AlbumCreation | null>(null);
  currentStep$ = this.currentStep.asObservable();
  songs$ = this.songs.asObservable();
  currentSong$ = this.currentSong.asObservable();
  createdAlbum$ = this.createdAlbum.asObservable();

  setCurrentStep(value: number) {
    this.currentStep.next(value);
  }

  initializeSongs(numberOfSongs: number) {
    const songs = Array.from(Array(numberOfSongs)).map((_, i) => ({
      id: i,
      songAudio: null,
      songAuthor: null,
      songGenre: null,
      songImage: null,
      songName: null,
    } as SongData));
    this.songs.next(songs);
  }

  setCurrentSong(id: number) {
    const song = this.songs.value.find(song => song.id === id);
    if (!song) return;
    this.currentSong.next(song);
  }

  setSongAudios(value: FileList) {
    const updatedSongs = this.songs.value.map((song, index) => ({
      ...song,
      songAudio: value[index] || song.songAudio
    }));
    this.songs.next(updatedSongs);
  }

  getCurrentSong(): SongData | null {
    return this.currentSong.value;
  }

  setSongData(currentSong: SongData, songImage: File, songName: string, songGenre: Genre) {
    const foundSong = this.songs.value.find(song => song.id === currentSong.id);
    if (!foundSong) return;
    const updatedSongs = this.songs.value.map(song =>
      song.id == currentSong.id ? {
        ...song,
        songImage: songImage,
        songName: songName,
        songGenre: songGenre,
      } : {...song}
    );
    this.songs.next(updatedSongs);

  }

  setNextSong(currentSong: SongData) {
    const foundNext = this.songs.value.find(song => song.id === currentSong.id + 1);
    if (!foundNext) return false;
    this.currentSong.next(foundNext);
    return true;
  }

  clearAlbumCreation() {
    this.createdAlbum.next(null);
  }

  setCreatedAlbum(param: AlbumCreation) {
    this.createdAlbum.next(param);
  }

  getCreatedAlbum() {
    return this.createdAlbum.value;
  }
}
