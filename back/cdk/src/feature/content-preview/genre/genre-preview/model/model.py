import dataclasses

@dataclasses.dataclass(slots=True,frozen=True)
class GenreArtistPreviewResponse:
    id: str
    name: str
    imageUrl: str

@dataclasses.dataclass(slots=True,frozen=True)
class GenreAlbumPreviewResponse:
    id: str
    title: str
    imageUrl: str
    performerNames:list[str]
    year:str
@dataclasses.dataclass(slots=True,frozen=True)
class GenreSongPreviewResponse:
    id: str
    name:str
    imageUrl: str

@dataclasses.dataclass(slots=True,frozen=True)
class GenrePreviewResponse:
    id: str
    name: str
    description: str
    imageUrl: str
    artists:list[GenreArtistPreviewResponse]
    albums:list[GenreAlbumPreviewResponse]
    songs:list[GenreSongPreviewResponse]
