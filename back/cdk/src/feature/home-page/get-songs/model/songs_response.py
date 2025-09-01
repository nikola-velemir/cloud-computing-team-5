from dataclasses import dataclass
from typing import List


@dataclass
class Song:
    id: int
    name: str
    imageUrl:str
    songUrl:str

@dataclass
class SongsResponse:
    songs: List[Song]
    lastToken: str
