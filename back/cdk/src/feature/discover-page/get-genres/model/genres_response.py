from dataclasses import dataclass
from typing import List


@dataclass
class Genre:
    id: str
    name: str

@dataclass
class GenresResponse:
    genres: List[Genre]