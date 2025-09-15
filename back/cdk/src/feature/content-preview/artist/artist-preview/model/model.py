import dataclasses


@dataclasses.dataclass
class ArtistViewAlbumResponse:
    id: str
    title: str
    year: str
    imageUrl: str


@dataclasses.dataclass
class ArtistViewSongResponse:
    id: str
    name: str
    imageUrl: str


@dataclasses.dataclass
class ArtistViewResponse:
    id: str
    name: str
    biography: str
    imageUrl: str
    songs: list[ArtistViewSongResponse]
    albums: list[ArtistViewAlbumResponse]
