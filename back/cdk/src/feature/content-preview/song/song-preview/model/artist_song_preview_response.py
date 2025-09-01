import dataclasses


@dataclasses.dataclass
class ArtistSongPreviewResponse:
    id:str
    name:str
    imageUrl:str