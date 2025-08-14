import {Injectable} from '@angular/core';
import {BehaviorSubject} from 'rxjs';
import {Genre} from '../model/genre';

@Injectable({
  providedIn: 'root'
})
export class ContentCreationService {
  private currentStep = new BehaviorSubject(0);
  private genre = new BehaviorSubject<Genre | null>(null);
  private songImage = new BehaviorSubject<File | null>(null);
  private songName = new BehaviorSubject<string | null>(null);
  private songFile = new BehaviorSubject<File | null>(null);
  genre$ = this.genre.asObservable();
  currentStep$ = this.currentStep.asObservable();
  songImage$ = this.songImage.asObservable();
  songName$ = this.songName.asObservable();
  songFile$ = this.songFile.asObservable();

  setGenre(genre: Genre) {
    this.genre.next(genre);
  }

  setSongImage(songImage: File | null): void {
    this.songImage.next(songImage);
  }

  constructor() {
  }

  nextStep() {
    this.currentStep.next(this.currentStep.getValue() + 1);
  }

  setSongName(value: string | null): void {
    this.songName.next(value);
  }

  setSongFile(value: File) {
    this.songFile.next(value);
  }
}
