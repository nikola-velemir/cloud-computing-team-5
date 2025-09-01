from dataclasses import dataclass



@dataclass
class AlbumRecord:
    PK: str
    Title: str
    GenreIds: list[str]
    ArtistIds: list[str]
    ReleaseDate: str
    ImageType: str
    SK: str = 'METADATA'