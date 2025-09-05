import dataclasses


@dataclasses.dataclass
class ArtistAlbumPreviewResponse:
    id: str
    name: str
    imageUrl: str

@dataclasses.dataclass
class SongAlbumPreviewResponse:
    id: str
    name: str
    imageUrl: str


@dataclasses.dataclass
class AlbumPreviewResponse:
    id: str
    imageUrl: str
    title: str
    releaseDate: str
    artists: list[ArtistAlbumPreviewResponse]
    songs:list[SongAlbumPreviewResponse]
