import { Injectable } from '@angular/core';
import { AudioApi } from '../../content-audio-player/service/audio-api.service';

@Injectable({
  providedIn: 'root',
})
export class DownloadService {
  constructor(private audioApi: AudioApi) {}

  downloadSong(songId: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.audioApi.getTrack(songId).subscribe({
        next: (track) => {
          if (!track.audioUrl) {
            resolve();
            return;
          }

          fetch(track.audioUrl)
            .then((res) => res.blob())
            .then((blob) => {
              const url = window.URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `${track.name || 'track'}.mp3`;
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
              window.URL.revokeObjectURL(url);
              resolve();
            })
            .catch((err) => {
              console.error('Download failed', err);
              reject(err);
            });
        },
        error: (err) => reject(err),
      });
    });
  }
}
