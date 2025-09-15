from dataclasses import dataclass
from typing import List


@dataclass
class Song:
    Id: int
    Name: str
    CoverImage: str

@dataclass
class SongsResponse:
    songs: List[Song]

