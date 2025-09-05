from dataclasses import dataclass


@dataclass
class Album:
    id: str
    title: str
    year: int
    imageUrl:str


@dataclass
class AlbumsResponse:
    albums: list[Album]
    lastToken: str