from dataclasses import dataclass


@dataclass(slots=True)
class GenreRecord:
    Name: str
    Id: str
    CoverPath: str


@dataclass(slots=True)
class ArtistRecord:
    Id:str
    ImagePath: str
    FirstName: str
    LastName: str
    Name: str


@dataclass(slots=True)
class AlbumRecord:
    Id: str
    CoverPath: str
    Title: str


@dataclass(slots=True)
class SongMetadataRecord:
    PK: str
    Name: str
    Genre: GenreRecord
    Artists: list[ArtistRecord]
    ReleaseDate: str
    Album: AlbumRecord
    AudioPath: str
    CoverPath: str
    CreatedAt: str
    Duration: int
    SK: str = 'METADATA'


@dataclass(slots=True)
class AlbumSongRecord:
    Id: str
    Name: str
    ReleaseDate: str
    AudioPath: str
    CoverPath: str
    CreatedAt: str
    Duration: int