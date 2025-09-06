from dataclasses import dataclass
from typing import List


@dataclass
class Album:
    id: str
    title: str

@dataclass
class AlbumsResponse:
    albums: List[Album]