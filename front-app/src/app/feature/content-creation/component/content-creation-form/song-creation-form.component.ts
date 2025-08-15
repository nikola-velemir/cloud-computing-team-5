import {Component, OnInit} from '@angular/core';
import {ContentCreationService} from '../../service/content-creation.service';
import {of, take} from 'rxjs';

@Component({
  selector: 'app-content-creation-form',
  standalone: false,
  templateUrl: './song-creation-form.component.html',
  styleUrl: './song-creation-form.component.scss'
})
export class SongCreationForm implements OnInit {

  currentStep$ = of(0);
  currentStep = 0;

  constructor(private contentCreationService: ContentCreationService) {
  }

  ngOnInit(): void {
    this.currentStep$ = this.contentCreationService.currentStep$

    this.currentStep$.subscribe(step => this.currentStep = step);
  }

  fileSelected($event: File) {
    console.log($event)
  }
}
