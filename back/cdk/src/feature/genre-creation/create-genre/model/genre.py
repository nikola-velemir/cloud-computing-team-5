from dataclasses import dataclass


@dataclass(slots=True)
class Genre:
    PK: str
    Name: str
    Description: str
    CoverPath: str
    Songs: list[{}]
    Albums: list[{}]
    SK: str = 'METADATA'
