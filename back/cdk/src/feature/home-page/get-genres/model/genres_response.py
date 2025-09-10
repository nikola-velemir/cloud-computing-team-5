from dataclasses import dataclass
from typing import List


@dataclass
class Genre:
    id: int
    name: str
    imageUrl:str

@dataclass
class GenresResponse:
    genres: List[Genre]
    lastToken: str
