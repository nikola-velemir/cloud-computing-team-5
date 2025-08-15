import {Component} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Author} from '../../model/author';
import {Album} from '../../model/album';

@Component({
  selector: 'content-creation-performer-album-step',
  standalone: false,
  templateUrl: './performer-album-step.html',
  styleUrl: './performer-album-step.scss'
})
export class PerformerAlbumStep {
    performerAlbumForm = new FormGroup({
      performer: new FormControl<Author | null>(null, [Validators.required]),
      albumRequired: new FormControl(false,[Validators.required]),
      album: new FormControl<Album | null>(null, [Validators.required]),
    })
}
