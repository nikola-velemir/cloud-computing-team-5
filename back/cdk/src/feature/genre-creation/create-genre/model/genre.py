from dataclasses import dataclass


@dataclass(slots=True)
class Genre:
    PK: str
    Name: str
    Description: str
    CoverPath: str
    Songs: dict[str,{}]
    Albums: dict[str,{}]
    UpdatedAt:str
    SK: str = 'METADATA'
    EntityType = 'GENRE'
