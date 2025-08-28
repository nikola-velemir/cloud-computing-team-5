from dataclasses import dataclass



@dataclass
class Album:
    PK: str
    Title: str
    GenreIds: list[str]
    SK: str = 'METADATA'