import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { Genre } from '../model/genre';
import { Artist } from '../model/artist';
import { AlbumCreation } from '../model/albumCreation';

export interface SongData {
  id: number;
  songAudio: File | null | undefined;
  songDuration: number;
  songImage: File | null | undefined;
  songName: string | null | undefined;
  songGenre: Genre | null | undefined;
  artists: Artist[];
}

@Injectable({
  providedIn: 'root',
})
export class ContentCreationService {
  getCurrentAlbum() {
    return this.albumId.value;
  }
  setArtists(arg0: Artist[]) {
    const updatedSongs = this.songs.value.map((s) => ({
      ...s,
      artists: [...arg0],
    }));
    this.songs.next(updatedSongs);
  }
  private currentStep = new BehaviorSubject(0);
  private currentSong = new BehaviorSubject<SongData | null>(null);
  private songs = new BehaviorSubject<SongData[]>([]);
  private albumId = new BehaviorSubject<string | null>(null);
  private createdAlbum = new BehaviorSubject<AlbumCreation | null>(null);
  currentStep$ = this.currentStep.asObservable();
  songs$ = this.songs.asObservable();
  currentSong$ = this.currentSong.asObservable();
  createdAlbum$ = this.createdAlbum.asObservable();

  setCurrentStep(value: number) {
    this.currentStep.next(value);
  }

  initializeSongs(numberOfSongs: number) {
    const songs = Array.from(Array(numberOfSongs)).map(
      (_, i) =>
        ({
          id: i,
          songAudio: null,
          artists: [],
          songDuration: 0,
          songGenre: null,
          songImage: null,
          songName: null,
        } as SongData)
    );
    this.songs.next(songs);
  }

  setCurrentSong(id: number) {
    const song = this.songs.value.find((song) => song.id === id);
    if (!song) return;
    this.currentSong.next(song);
  }

  setSongAudios(value: { file: File; duration: number }[]) {
    const updatedSongs = this.songs.value.map((song, index) => ({
      ...song,
      songAudio: value[index] ? value[index].file : song.songAudio,
      songDuration: value[index] ? value[index].duration : song.songDuration,
    }));
    this.songs.next(updatedSongs);
  }

  getCurrentSong(): SongData | null {
    return this.currentSong.value;
  }

  setSongData(
    currentSong: SongData,
    songImage: File,
    songName: string,
    songGenre: Genre
  ) {
    const foundSong = this.songs.value.find(
      (song) => song.id === currentSong.id
    );
    if (!foundSong) return;
    const updatedSongs = this.songs.value.map((song) =>
      song.id == currentSong.id
        ? {
            ...song,
            songImage: songImage,
            songName: songName,
            songGenre: songGenre,
          }
        : { ...song }
    );
    this.songs.next(updatedSongs);
  }

  setNextSong(currentSong: SongData) {
    const foundNext = this.songs.value.find(
      (song) => song.id === currentSong.id + 1
    );
    if (!foundNext) return false;
    this.currentSong.next(foundNext);
    return true;
  }

  clearAlbumCreation() {
    this.createdAlbum.next(null);
  }

  setCreatedAlbum(param: AlbumCreation) {
    this.createdAlbum.next(param);
    this.albumId.next(null);
  }

  getCreatedAlbum() {
    return this.createdAlbum.value;
  }
  getSongs() {
    return this.songs.value;
  }
  setExistingAlbum(id: string): void {
    this.albumId.next(id);
    this.createdAlbum.next(null);
  }
  getArtists(): Artist[] {
    const allIds = this.songs.value.map((song) => song.artists).flat();

    // Remove duplicates
    return Array.from(new Set(allIds));
  }
}
