import dataclasses


@dataclasses.dataclass
class AlbumResponse:
    id:str
    tracks:list[str]