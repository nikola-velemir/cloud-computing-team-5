from dataclasses import dataclass


@dataclass
class SongMetadataRecord:
    Id: str
    Name: str
    ReleaseDate: str
    AudioPath:str
    CoverPath: str
    EntityType = 'SONG'

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
    UpdatedAt:str
    Genres: dict[str,GenreRecord]
    Songs:dict[str,SongMetadataRecord]
    Artists:dict[str,ArtistRecord]
    SK: str = 'METADATA'
    EntityType = 'ALBUM'

@dataclass
class GenreAlbumRecord:
    Id: str
    Title: str
    ReleaseDate: str
    CoverPath: str