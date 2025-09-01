import dataclasses


@dataclasses.dataclass
class AlbumSongPreviewResponse:
    id:str
    imageUrl:str
    title:str
    year:str
