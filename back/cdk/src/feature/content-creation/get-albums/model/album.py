from dataclasses import dataclass


@dataclass
class AlbumResponse:
    id: str
    title: str
    year: int
    artistIds:list[str]
    imageUrl:str
