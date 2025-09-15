import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { forkJoin, map, of, switchMap } from 'rxjs';
import { environment } from '../../../../environments/environement';
import { SongData } from './content-creation.service';

export interface AlbumCoverUploadRequest {
  albumId: string;
  contentType: string;
}
export interface SongUploadRequest {
  songId: string;
  contentType: string;
  type: 'cover' | 'audio';
}
export interface CreateAlbumRequest {
  genreIds: string[];
  title: string;
  artistIds: string[];
  releaseDate: string;
  imageType: string;
}
export interface UploadFile {
  url: string;
  file: File;
  contentType: string;
}
export interface CreateSongAsSingleRequest {
  name: string;
  genreId: string;
  artistIds: string[];

  duration: number;
  imageType: string;
  audioType: string;
}
export interface CreateSongWithAlbumRequest {
  name: string;
  genreId: string;
  artistIds: string[];
  albumId: string;
  imageType: string;
  audioType: string;
  duration: number;
}

interface SongMetadataResponse {
  songId: string;
  songName: string;
  genreId: string;
}

@Injectable({
  providedIn: 'root',
})
export class ContentCreationApi {
  private readonly URL = environment.apiUrl + '/content-creation';
  constructor(private http: HttpClient) {}

  createAsSingles() {}

  createOnNewAlbum() {
    return of(1);
  }
  private requestAlbumCoverUploadUrl(payload: AlbumCoverUploadRequest) {
    return this.http.put<{ uploadUrl: string }>(this.URL + '/albums', payload);
  }
  private uploadAlbumCover(url: string, file: File, contentType: string) {
    return this.http.put(url, file, {
      headers: {
        'Content-Type': file.type || 'application/octet-stream',
      },
    });
  }
  private requestSongUploadUrl(payload: SongUploadRequest) {
    return this.http.put<{ uploadUrl: string }>(this.URL + '/songs', payload);
  }
  private uploadSongFiles(files: UploadFile[]) {
    const uploadRequests = files.map(({ url, file, contentType }) =>
      this.http.put(url, file, {
        headers: { 'Content-Type': contentType || 'application/octet-stream' },
        observe: 'response', // if you want full response, optional
      })
    );

    return forkJoin(uploadRequests);
  }

  private requestSongUrls(
    songResponse: SongMetadataResponse,
    contentTypeAudio: string,
    contentTypeImage: string
  ) {
    const audioUrlRequest$ = this.requestSongUploadUrl({
      songId: songResponse.songId,
      contentType: contentTypeAudio,
      type: 'audio',
    });
    const imageUrlRequest$ = this.requestSongUploadUrl({
      songId: songResponse.songId,
      contentType: contentTypeImage,
      type: 'cover',
    });
    return forkJoin({
      imageUrl: imageUrlRequest$,
      audioUrl: audioUrlRequest$,
    });
  }
  createSongAsSingle(
    song: CreateSongAsSingleRequest,
    audioFile: File,
    imageFile: File
  ) {
    const contentTypeAudio = audioFile.type || 'audio/mpeg';
    const contentTypeImage = imageFile.type || 'image/jpeg';

    const songRequest$ = this.http.post<SongMetadataResponse>(
      this.URL + '/songs/create-as-single',
      song
    );

    return songRequest$.pipe(
      switchMap((songResp) => {
        return this.requestSongUrls(
          songResp,
          contentTypeAudio,
          contentTypeImage
        ).pipe(
          switchMap(({ audioUrl, imageUrl }) => {
            const files: UploadFile[] = [
              {
                url: audioUrl.uploadUrl,
                file: audioFile,
                contentType: contentTypeAudio,
              },
              {
                url: imageUrl.uploadUrl,
                file: imageFile,
                contentType: contentTypeImage,
              },
            ];

            return this.uploadSongFiles(files);
          })
        );
      })
    );
  }
  createSongWithAlbum(
    song: CreateSongWithAlbumRequest,
    audioFile: File,
    imageFile: File
  ) {
    const contentTypeAudio = audioFile.type || 'audio/mpeg';
    const contentTypeImage = imageFile.type || 'image/jpeg';

    const songRequest$ = this.http.post<SongMetadataResponse>(
      this.URL + '/songs/create-with-album',
      song
    );

    return songRequest$.pipe(
      switchMap((songResp) => {
        return this.requestSongUrls(
          songResp,
          contentTypeAudio,
          contentTypeImage
        ).pipe(
          switchMap(({ audioUrl, imageUrl }) => {
            const files: UploadFile[] = [
              {
                url: audioUrl.uploadUrl,
                file: audioFile,
                contentType: contentTypeAudio,
              },
              {
                url: imageUrl.uploadUrl,
                file: imageFile,
                contentType: contentTypeImage,
              },
            ];

            return this.uploadSongFiles(files);
          })
        );
      })
    );
  }
  createAlbum(request: CreateAlbumRequest, file: File) {
    const albumRequest = this.http.post<{ albumId: string }>(
      this.URL + '/albums',
      request
    );

    return albumRequest.pipe(
      switchMap((v) => {
        const albumId = v.albumId;
        const contentType = file.type || 'application/octet-stream';

        return this.requestAlbumCoverUploadUrl({
          albumId: v.albumId,
          contentType,
        }).pipe(
          switchMap((res) =>
            this.uploadAlbumCover(res.uploadUrl, file, contentType).pipe(
              map(() => albumId)
            )
          )
        );
      })
    );
  }
  createWithAlbum(formData: FormData) {
    return this.http.post(this.URL + '/songs/with-album', formData);
  }
}
