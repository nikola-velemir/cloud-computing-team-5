from dataclasses import dataclass


@dataclass(slots=True)
class Artist:
    PK: str
    Name: str
    Biography: str
    UpdatedAt: str
    Songs: dict[str,{}]
    Albums: dict[str,{}]
    Genres: dict[str,{}]
    SK: str = 'METADATA'

@dataclass(slots=True)
class GenreDTO:
    Id: str
    Name: str
    Image: str
