import dataclasses

from artist_song_preview_response import ArtistSongPreviewResponse
from album_song_preview_response import AlbumSongPreviewResponse

@dataclasses.dataclass
class SongPreviewResponse:
    id:str
    name:str
    artists:list[ArtistSongPreviewResponse]
    album: AlbumSongPreviewResponse
    imageUrl:str
