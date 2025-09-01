from dataclasses import dataclass



@dataclass
class AlbumRecord:
    PK: str
    Title: str
    GenreIds: list[str]
    ArtistIds: list[str]
    ReleasedDate: str
    ImageType: str
    SK: str = 'METADATA'