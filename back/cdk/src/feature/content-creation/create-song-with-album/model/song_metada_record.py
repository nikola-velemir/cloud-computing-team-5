from dataclasses import dataclass


@dataclass
class SongMetadataRecord:
    PK: str
    Name: str
    GenreId: str
    ArtistIds: list[str]
    ReleaseDate: str
    AlbumId: str
    ImageType: str
    SK: str = 'METADATA'
