from dataclasses import dataclass



@dataclass
class Album:
    PK: str
    Title: str
    GenreIds: list[str]
    ArtistIds: list[str]
    SK: str = 'METADATA'