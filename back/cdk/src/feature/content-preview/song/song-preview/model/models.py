import dataclasses

@dataclasses.dataclass
class ArtistSongPreviewResponse:
    id:str
    name:str
    imageUrl:str

@dataclasses.dataclass
class AlbumSongPreviewResponse:
        id: str
        imageUrl: str
        title: str
        year: str

@dataclasses.dataclass
class SongPreviewResponse:
    id:str
    name:str
    artists:list[ArtistSongPreviewResponse]
    album: AlbumSongPreviewResponse
    imageUrl:str
