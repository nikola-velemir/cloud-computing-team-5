from dataclasses import dataclass


@dataclass
class AlbumResponse:
    id: str
    title: str
    year: int
    imageUrl: str
