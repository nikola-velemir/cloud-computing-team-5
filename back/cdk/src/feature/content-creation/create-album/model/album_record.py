from dataclasses import dataclass


@dataclass
class SongMetadataRecord:
    Id: str
    Name: str
    ReleaseDate: str
    AudioPath:str
    CoverPath: str

@dataclass
class GenreRecord:
    Id: str
    Name: str
    CoverPath: str
@dataclass
class ArtistRecord:
    Id: str
    Name: str
    FirstName: str
    LastName: str
    ImagePath: str
@dataclass
class AlbumRecord:
    PK: str
    Title: str
    ReleaseDate: str
    CoverPath:str
    Genres: list[GenreRecord]
    Songs:list[SongMetadataRecord]
    Artists:list[ArtistRecord]
    SK: str = 'METADATA'